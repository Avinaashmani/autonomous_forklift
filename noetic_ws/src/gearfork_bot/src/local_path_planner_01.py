#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def create_spline_for_first_two_points(corners):
    # Extract x, y coordinates and tangent values (orientations) for the first two points
    x = np.array([corners[0][0], corners[1][0]])
    y = np.array([corners[0][1], corners[1][1]])
    tangents = np.array([corners[0][2], corners[1][2]])

    # Calculate the tangents (dy/dx)
    tangent_values = np.tan(tangents)

    # Create the cubic spline with tangents
    x_interp = np.linspace(x[0], x[1], 100)
    cs = CubicSpline(x, y, bc_type=((1, tangent_values[0]), (1, tangent_values[1])))
    y_interp = cs(x_interp)

    # Plotting
    plt.plot(x, y, "o", label="Data Points")
    plt.plot(x_interp, y_interp, "black", label="Cubic Spline")
    plt.legend()
    plt.show()

    # Return interpolated points
    return x_interp, y_interp

def create_square_path(side_length):
    path = Path()
    path.header.frame_id = "map"
    path.header.stamp = rospy.Time.now()

    # Define the four corners of the square with slight rotations
    corners = [
        (0, 0, 0),
        (side_length, 0, np.deg2rad(23)),
        (side_length, side_length, np.deg2rad(3)),
        (0, side_length, np.deg2rad(9)),
        (0, 0, 0)
    ]
    
    # Create and plot the spline for the first two points
    x_interp, y_interp = create_spline_for_first_two_points(corners)
    
    # Add interpolated points to the path
    for x, y in zip(x_interp, y_interp):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0
        pose.pose.orientation.w = 1.0  # Neutral orientation (no rotation)
        path.poses.append(pose)

    return path

def publish_square_path():
    rospy.init_node('square_path_publisher')
    path_pub = rospy.Publisher('/path', Path, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    side_length = 3.0  # 3 meters

    while not rospy.is_shutdown():
        square_path = create_square_path(side_length)
        path_pub.publish(square_path)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_square_path()
    except rospy.ROSInterruptException:
        pass
