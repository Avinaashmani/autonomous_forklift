#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import numpy as np
from scipy.interpolate import CubicSpline

class PathPlanner:
    def __init__(self):
        rospy.init_node("path_planner")
        rospy.loginfo_once("Path Planner Experiment")

        # Define the corners (waypoints) of the path
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

        # Preprocess corners to ensure strictly increasing x values
        self.processed_points = self.preprocess_points(self.corners)
        
        self.path_pub = rospy.Publisher('/move_base/GlobalPlanner/plan', Path, queue_size=10)
        
        self.publish_path()

    def preprocess_points(self, corners):
        # Sort points based on the x values to ensure they are strictly increasing
        sorted_corners = sorted(corners, key=lambda point: point[0])

        # Remove duplicates and ensure strictly increasing x values
        processed_points = [sorted_corners[0]]
        for point in sorted_corners[1:]:
            if point[0] > processed_points[-1][0]:
                processed_points.append(point)
        
        return np.array(processed_points)

    def publish_path(self):
        # Generate smooth path using cubic splines
        points = self.processed_points
        x = points[:, 0]
        y = points[:, 1]

        cs = CubicSpline(x, y)
        xs = np.linspace(x.min(), x.max(), 100)
        ys = cs(xs)

        # Publish the smooth path
        path_msg = Path()
        path_msg.header.frame_id = "map"
        path_msg.header.stamp = rospy.Time.now()

        for x, y in zip(xs, ys):
            pose_msg = PoseStamped()
            pose_msg.header.frame_id = "map"
            pose_msg.header.stamp = rospy.Time.now()
            pose_msg.pose.position.x = x
            pose_msg.pose.position.y = y
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
