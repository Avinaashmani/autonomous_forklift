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

        # Control points for a dollar sign shape
        self.x = np.array([-5, -2.5, -1.5, 0, 1.5, 2.5, 5])
        self.y = np.array([0, 0.5, 0.5, 2, 3, 4, 5])

        self.points = None
        self.side_length = 5
        self.corners = [
            (0, 0),
            (-self.side_length, 0),
            (self.side_length, self.side_length),
            (0, self.side_length),
            (0, 0)
        ]
        
        self.path_pub = rospy.Publisher('/path', Path, queue_size=10)
        self.curved_path_pub = rospy.Publisher('/curved_path', Path, queue_size=10)

        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.compute)

        self.plot_spline()

    def plot_spline(self):
        x_interp = np.linspace(self.x[0], self.x[-1], 100)
        cs = CubicSpline(self.x, self.y, bc_type="natural")
        y_interp = cs(x_interp)
        
        self.points = list(zip(x_interp, y_interp))
        print(self.points)

        plt.plot(self.x, self.y, "o", label="Control Points")
        plt.plot(x_interp, y_interp, "black", label="Cubic Spline")
        plt.legend()
        plt.show()

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

        # Publish curved path
        curved_path_msg = Path()
        curved_path_msg.header.frame_id = "map"
        curved_path_msg.header.stamp = rospy.Time.now()

        for point in self.points:
            pose_msg_curve = PoseStamped()
            pose_msg_curve.header.frame_id = "map"
            pose_msg_curve.header.stamp = rospy.Time.now()

            pose_msg_curve.pose.position.x = point[0]
            pose_msg_curve.pose.position.y = point[1]
            pose_msg_curve.pose.orientation.w = 1.0  # Default orientation

            curved_path_msg.poses.append(pose_msg_curve)

        self.curved_path_pub.publish(curved_path_msg)


if __name__ == '__main__':
    try:
        planner = PathPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
