#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

class PathPlanner:
    def __init__(self):
        rospy.init_node("path_planner")
        rospy.loginfo_once("Path Planner Experiment")

        self.points = None
        self.side_length = 5
        self.corners = [
            (0.53, 0.0),
            (0.53, 4.0),
            (0.0, 0.05),
            (-8.36, 0.05),
            (-8.36, 4.0),
            (-8.36, 0.05),
            (-16.0, 0.05),
            (-16.0, 4.0)
        ]
        
        self.path_pub = rospy.Publisher('/move_base/TebLocalPlannerROS/global_plan', Path, queue_size=10)
        self.curved_path_pub = rospy.Publisher('/curved_path', Path, queue_size=10)

        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.compute)

    def compute(self, event):
        # Publish original path
        path_msg = Path()
        path_msg.header.frame_id = "map"
        path_msg.header.stamp = rospy.Time.now()

        for corner in self.corners:
            pose_msg = PoseStamped()
            pose_msg.header.frame_id = "map"
            pose_msg.header.stamp = rospy.Time.now()
            pose_msg.pose.position.x = corner[0]
            pose_msg.pose.position.y = corner[1]
            pose_msg.pose.orientation.z = 1.0
            pose_msg.pose.orientation.w = 1.0

            path_msg.poses.append(pose_msg)

        self.path_pub.publish(path_msg)

if __name__ == '__main__':
    try:
        planner = PathPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
