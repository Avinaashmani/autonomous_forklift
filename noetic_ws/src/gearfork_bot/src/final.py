#!/usr/bin/env python3

# Import necessary ROS and other Python libraries
import rospy
from geometry_msgs.msg import Twist, Point, Quaternion
import tf
from math import radians, copysign, sqrt, pow, pi, atan2
from tf.transformations import euler_from_quaternion
import numpy as np
import subprocess
import os
import time
import math 
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from tf.transformations import quaternion_from_euler

# PID controller constants for distance and angle
kp_distance = 1
ki_distance = 0.01
kd_distance = 0.5

kp_angle = 1
ki_angle = 0.03
kd_angle = 0.05

class GotoPoint():
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('turtlebot3_pointop_key', anonymous=False)

        # Register the shutdown function (cleanup function) to be called when the node is terminated
        rospy.on_shutdown(self.shutdown)

        # Publisher for the robot's velocity commands
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=5)

        # Initialize variables for position and velocity commands
        position = Point()
        move_cmd = Twist()

        self.pallet_position = 0.0
        self.pallet_x = 0.0
        self.pallet_y = 0.0
        self.pallet_angle = 0.0

        # Set the rate at which the loop operates
        r = rospy.Rate(10)

        # Initialize the TransformListener to listen for transformations
        self.tf_listener = tf.TransformListener()

        # Define the reference frame for odometry
        self.odom_frame = 'odom'

        # Attempt to find the transformation between 'odom' and 'base_footprint'
        try:
            self.tf_listener.waitForTransform(self.odom_frame, 'base_footprint', rospy.Time(), rospy.Duration(1.0))
            self.tf_listener.waitForTransform('/odom', '/pallet_center', rospy.Time(), rospy.Duration(1.0))
            self.base_frame = 'base_footprint'
        
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            # If unsuccessful, attempt to find the transformation between 'odom' and 'base_link'
            try:
                self.tf_listener.waitForTransform(self.odom_frame, 'base_link', rospy.Time(), rospy.Duration(1.0))
                self.tf_listener.waitForTransform('/odom', '/pallet_center', rospy.Time(), rospy.Duration(1.0))
                self.base_frame = 'base_link'
            except (tf.Exception, tf.ConnectivityException, tf.LookupException):
                # If still unsuccessful, log the error and shutdown the node
                rospy.loginfo("Cannot find transform between odom and base_link or base_footprint")
                rospy.signal_shutdown("tf Exception")

        # Get the initial position and rotation of the robot
        (position, rotation) = self.get_odom()

        # Initialize variables for the robot's last rotation, speed, and goal position
        last_rotation = 0
        linear_speed = 1  # Proportional gain for distance
        angular_speed = 1  # Proportional gain for angle

        # Get the target coordinates and angle from the user
        (goal_x, goal_y, goal_z) = self.pallet_x, self.pallet_y, self.pallet_angle
        
        goal_z = np.deg2rad(goal_z)  # Convert degrees to radians

        # Calculate the distance to the goal
        goal_distance = sqrt(pow(goal_x - position.x, 2) + pow(goal_y - position.y, 2))
        distance = goal_distance  # Initialize the error for distance

        # Initialize variables for PID control
        previous_distance = 0
        total_distance = 0
        previous_angle = 0
        total_angle = 0

        # Loop until the robot is within 5 cm of the target
        while distance > 0.05:
            # Get the current position and rotation of the robot
            (position, rotation) = self.get_odom()
            x_start = position.x
            y_start = position.y

            # Calculate the angle to the goal
            path_angle = atan2(goal_y - y_start, goal_x - x_start)

            # Adjust path_angle if it crosses boundaries
            if path_angle < -pi/4 or path_angle > pi/4:
                if goal_y < 0 and y_start < goal_y:
                    path_angle = -2*pi + path_angle
                elif goal_y >= 0 and y_start > goal_y:
                    path_angle = 2*pi + path_angle

            # Adjust rotation if it crosses boundaries
            if last_rotation > pi-0.1 and rotation <= 0:
                rotation = 2*pi + rotation
            
            elif last_rotation < -pi+0.1 and rotation > 0:
                rotation = -2*pi + rotation

            # Calculate the difference in angle and distance
            diff_angle = path_angle - previous_angle
            diff_distance = distance - previous_distance

            # Recalculate the distance to the goal
            distance = sqrt(pow((goal_x - x_start), 2) + pow((goal_y - y_start), 2))

            # Calculate control signals for distance and angle using PID control
            control_signal_distance = kp_distance*distance + ki_distance*total_distance + kd_distance*diff_distance
            control_signal_angle = kp_angle*path_angle + ki_angle*total_angle + kd_angle*diff_angle

            # Update the movement command
            move_cmd.angular.z = (control_signal_angle) - rotation
            move_cmd.linear.x = -min(control_signal_distance, 0.1) # Limit the linear speed

            # Limit the angular speed
            if move_cmd.angular.z > 0:
                move_cmd.angular.z = min(move_cmd.angular.z, 1.5)
            else:
                move_cmd.angular.z = max(move_cmd.angular.z, -1.5)

            # Update last rotation
            last_rotation = rotation

            # Publish the velocity commands
            self.cmd_vel.publish(move_cmd)

            # Sleep to maintain the loop rate
            r.sleep()

            # Update previous and total distances
            previous_distance = distance
            total_distance += distance

            # Print current position and rotation for debugging
            print("Current position and rotation are: ", (position, rotation))

        # Final check for the position and rotation
        (position, rotation) = self.get_odom()
        print("Current position and rotation are: ", (position, rotation))
        print("Reached :)   ^_^")

        # Adjust the final angle if necessary
        while abs(rotation - goal_z) > 0.05:
            (position, rotation) = self.get_odom()
            if goal_z >= 0:
                if rotation <= goal_z and rotation >= goal_z - pi:
                    move_cmd.linear.x = 0.00
                    move_cmd.angular.z = 0.5
                else:
                    move_cmd.linear.x = 0.00
                    move_cmd.angular.z = -0.5
            else:
                if rotation <= goal_z + pi and rotation > goal_z:
                    move_cmd.linear.x = 0.00
                    move_cmd.angular.z = -0.5
                else:
                    move_cmd.linear.x = 0.00
                    move_cmd.angular.z = 0.5
            self.cmd_vel.publish(move_cmd)
            r.sleep()

        # Stop the robot after reaching the goal
        self.cmd_vel.publish(Twist())
        return

    def get_odom(self):
        # Get the current odometry information (position and rotation)
        try:
            (trans, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
            (trans_pallet, rot_pallet) = self.tf_listener.lookupTransform('/odom', '/pallet_center', rospy.Time(0))
            
            rotation = euler_from_quaternion(rot)
            rotation_pallet = euler_from_quaternion(rot_pallet)

            self.pallet_position = Point(*trans_pallet)
            self.pallet_x = self.pallet_position.x
            self.pallet_y = self.pallet_position.y

        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return
        return (Point(*trans), rotation[2])

    def shutdown(self):
        # Publish zero velocity to stop the robot
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)



while not rospy.is_shutdown():
    GotoPoint()
