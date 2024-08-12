#!/usr/bin/env python3
import rospy
import csv
from nav_msgs.msg import Odometry
from mbf_msgs.msg import ExePathAction, ExePathGoal
from actionlib import SimpleActionClient
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import SetBool
from datetime import datetime
import threading
from std_msgs.msg import Header
from visualization_msgs.msg import Marker

class StraightLinePathPlanner:
    def __init__(self):
        rospy.init_node("straight_line_path_planner")
        rospy.loginfo("Straight Line Path Planner Started")

        self.goal_x = 0.0
        self.goal_y = 0.0
        self.goal_angle_z = 0.0
        self.goal_angle_w = 0.0
        self.goal_positions = None

        self.recording = False
        self.csv_file = None
        self.publish_thread = None

        self.initial_pose = None

        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_pose_cb)

        self.marker_pub = rospy.Publisher('/visualization_marker', Marker, queue_size=10)

        self.service = rospy.Service('/start_recording', SetBool, self.service_callback)
        self.service_2 = rospy.Service('/start_publishing', SetBool, self.publish_path)

    def odom_callback(self, msg):
        self.initial_pose = msg.pose.pose

    def service_callback(self, req):
        if req.data:
            rospy.loginfo("Starting to record poses")
            self.recording = True
            filename = datetime.now().strftime('/home/avinaash/autonomous_forklift/noetic_ws/src/forkamrtest3/path_plots/robot_poses_%Y%m%d_%H%M%S.csv')
            self.csv_file = open(filename, mode='w')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(['Time', 'X', 'Y', 'Orientation_Z', 'Orientation_W'])
        else:
            rospy.loginfo("Stopping recording")
            self.recording = False
            if self.csv_file:
                self.csv_file.close()
                self.csv_file = None
        return [True, "Service call successful"]

    def goal_pose_cb(self, msg):
        self.goal_x = round(msg.pose.position.x, 4)
        self.goal_y = round(msg.pose.position.y, 4)
        self.goal_angle_z = round(msg.pose.orientation.z, 4)
        self.goal_angle_w = round(msg.pose.orientation.w, 4)
        self.goal_positions = (self.goal_x, self.goal_y, self.goal_angle_z, self.goal_angle_w)
        if self.recording:
            self.record_pose()

    def record_pose(self):
        if self.csv_writer:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.csv_writer.writerow([current_time, self.goal_x, self.goal_y, self.goal_angle_z, self.goal_angle_w])
            rospy.loginfo(f"Recorded pose at {current_time}: x={self.goal_x}, y={self.goal_y}, z={self.goal_angle_z}, w={self.goal_angle_w}")
            self.publish_marker()

    def publish_marker(self):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "waypoints"
        marker.id = int(rospy.Time.now().to_sec() * 1000)  # unique ID
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = self.goal_x
        marker.pose.position.y = self.goal_y
        marker.pose.position.z = 0.0
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = self.goal_angle_z
        marker.pose.orientation.w = self.goal_angle_w
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        self.marker_pub.publish(marker)

    def publish_path(self, req):
        if self.initial_pose is None:
            rospy.logwarn_once("Waiting for Robot Odom...")

        if req.data:
            rospy.loginfo("Starting to publish path")
            if not self.publish_thread or not self.publish_thread.is_alive():
                self.publish_thread = threading.Thread(target=self.publish_path_once)
                self.publish_thread.start()
        else:
            rospy.loginfo("Publish path service called with False")
        return [True, "Service call successful"]

    def publish_path_once(self):
        file_name = input("Enter the File name (without extension): ")
        file_path = f"/home/avinaash/autonomous_forklift/noetic_ws/src/forkamrtest3/path_plots/{file_name}.csv"

        client = SimpleActionClient('/move_base_flex/exe_path', ExePathAction)
        client.wait_for_server()

        try:
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header row

                path_msg = ExePathGoal()
                path_msg.path.header.frame_id = 'map'

                for row in csv_reader:
                    pose_msg = PoseStamped()
                    pose_msg.header = Header()
                    pose_msg.header.frame_id = "map"
                    pose_msg.header.stamp = rospy.Time.now()
                    pose_msg.pose.position.x = float(row[1])
                    pose_msg.pose.position.y = float(row[2])
                    pose_msg.pose.position.z = 0.0
                    pose_msg.pose.orientation.z = float(row[3])
                    pose_msg.pose.orientation.w = float(row[4])
                    path_msg.path.poses.append(pose_msg)

                client.send_goal(path_msg)
                client.wait_for_result()
                result = client.get_result()
                rospy.loginfo("Result: %s", result)

        except FileNotFoundError:
            rospy.logerr(f"File {file_path} not found")

if __name__ == '__main__':
    try:
        planner = StraightLinePathPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
