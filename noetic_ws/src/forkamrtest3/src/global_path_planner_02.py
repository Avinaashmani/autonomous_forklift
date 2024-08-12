#!/usr/bin/env python3
import rospy
import csv
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import SetBool
from datetime import datetime
import threading

class StraightLinePathPlanner:
    def __init__(self):
        rospy.init_node("straight_line_path_planner")
        rospy.loginfo("Straight Line Path Planner Started")

        self.path_pub = rospy.Publisher('/path', Path, queue_size=10)

        self.goal_x = 0.0
        self.goal_y = 0.0
        self.goal_angle_z = 0.0
        self.goal_angle_w = 0.0
        self.goal_positions = None

        self.recording = False
        self.csv_file = None
        self.publish_thread = None
        self.keep_publishing = False

        rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_pose_cb)
        self.service = rospy.Service('/start_recording', SetBool, self.service_callback)
        self.service_2 = rospy.Service('/start_publishing', SetBool, self.publish_path)

    def service_callback(self, req):
        if req.data:
            rospy.loginfo("Starting to record poses")
            self.recording = True
            filename = datetime.now().strftime('/home/avinaash/autonomous_forklift/noetic_ws/src/gearfork_bot/map_points/robot_poses_%Y%m%d_%H%M%S.csv')
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
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.goal_angle_z = msg.pose.orientation.z
        self.goal_angle_w = msg.pose.orientation.w
        self.goal_positions = (self.goal_x, self.goal_y, self.goal_angle_z, self.goal_angle_w)
        if self.recording:
            self.record_pose()

    def record_pose(self):
        if self.csv_writer:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.csv_writer.writerow([current_time, self.goal_x, self.goal_y, self.goal_angle_z, self.goal_angle_w])
            rospy.loginfo(f"Recorded pose at {current_time}: x={self.goal_x}, y={self.goal_y}, z={self.goal_angle_z}, w={self.goal_angle_w}")

    def publish_path(self, req):
        if req.data:
            rospy.loginfo("Starting to publish path")
            self.keep_publishing = True
            if not self.publish_thread or not self.publish_thread.is_alive():
                self.publish_thread = threading.Thread(target=self.publish_path_loop)
                self.publish_thread.start()
        else:
            rospy.loginfo("Stopping publishing path")
            self.keep_publishing = False
        return [True, "Service call successful"]

    def publish_path_loop(self):
        file_name = input("Enter the File name (without extension): ")
        file_path = f"/home/avinaash/autonomous_forklift/noetic_ws/src/gearfork_bot/map_points/{file_name}.csv"
        while self.keep_publishing:
            try:
                with open(file_path, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    next(csv_reader)  # Skip header row
                    path_msg = Path()
                    path_msg.header.frame_id = "map"
                    path_msg.header.stamp = rospy.Time.now()
                    for row in csv_reader:
                        pose_msg = PoseStamped()
                        pose_msg.header.frame_id = "map"
                        pose_msg.header.stamp = rospy.Time.now()
                        pose_msg.pose.position.x = float(row[1])
                        pose_msg.pose.position.y = float(row[2])
                        pose_msg.pose.orientation.z = float(row[3])
                        pose_msg.pose.orientation.w = float(row[4])
                        path_msg.poses.append(pose_msg)
                    rospy.loginfo("Publishing path with %d waypoints", len(path_msg.poses))
                    self.path_pub.publish(path_msg)
                rospy.sleep(1)  # Publish at a 1-second interval
            except FileNotFoundError:
                rospy.logerr(f"File {file_path} not found")
                self.keep_publishing = False

if __name__ == '__main__':
    try:
        planner = StraightLinePathPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
