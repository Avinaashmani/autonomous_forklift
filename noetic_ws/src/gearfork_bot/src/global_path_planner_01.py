#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class StraightLinePathPlanner:
    def __init__(self):
        rospy.init_node("straight_line_path_planner")
        rospy.loginfo("Straight Line Path Planner Started")

        self.start_point = (0, 0)
        self.end_points = [(3.8, 0), (3.8, 1.5), (3.8, 0), (-2.5, 0), (-2.5, 1.5),( -2.5, 0), (-8.75, 0), (-8.75, 1.75)]
        self.waypoint_interval = 1.0  # Distance between waypoints

        self.path_pub = rospy.Publisher('/path', Path, queue_size=10)
        
        self.goal_x = 0.0
        self.goal_y = 0.0
        self.goal_angle_z = 0.0
        self.goal_angle_w = 0.0
        
        rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_pose_cb)
        self.compute_path()

    def compute_path(self):
        while True:
            path_msg = Path()
            path_msg.header.frame_id = "map"
            path_msg.header.stamp = rospy.Time.now()

            x0, y0 = self.start_point

            for x1, y1 in self.end_points:
                dx = x1 - x0
                dy = y1 - y0
                distance = ((dx**2) + (dy**2))**0.5
                num_waypoints = int(distance / self.waypoint_interval)

                for i in range(num_waypoints + 1):
                    if num_waypoints == 0:
                        t = 1
                    else:
                        t = i / float(num_waypoints)
                    x = x0 + t * dx
                    y = y0 + t * dy

                    pose_msg = PoseStamped()
                    pose_msg.header.frame_id = "map"
                    pose_msg.header.stamp = rospy.Time.now()
                    pose_msg.pose.position.x = x
                    pose_msg.pose.position.y = y
                    pose_msg.pose.orientation.z = 0.0
                    pose_msg.pose.orientation.w = 1.0

                    path_msg.poses.append(pose_msg)

                x0, y0 = x1, y1  # Update start point for the next segment

            rospy.loginfo("Publishing path with %d waypoints", len(path_msg.poses))
            self.path_pub.publish(path_msg)
    
    def goal_pose_cb(self, msg):
        self.goal_x = msg.pose.position.x 
        self.goal_y = msg.pose.position.y
        self.goal_angle_z = msg.pose.orientation.z
        self.goal_angle_w = msg.pose.orientation.w

if __name__ == '__main__':
    try:
        planner = StraightLinePathPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
