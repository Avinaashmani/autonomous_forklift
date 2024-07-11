#!/usr/bin/env python3

import rospy
import rosparam
import tf
import numpy as np
import matplotlib.pyplot as plt
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class DockPallet:

    def __init__(self):
        rospy.init_node('pallet_dock', anonymous=True)
        rosparam.load_file('/home/avinaash/autonomous_forklift/noetic_ws/src/gearfork_bot/config/pallet_docking_prams.yaml')

        self.pallet_x = 0.0
        self.pallet_y = 0.0
        self.pallet_angle = 0.0

        self.fork_x = 0.0
        self.fork_y = 0.0
        self.fork_angle = 0.0

        self.get_initial_x = 0.0
        self.get_initial_y = 0.0
        self.initial_position = None

        self.tf_listener = tf.TransformListener()

        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.control_loop)
        rospy.loginfo("Initialized DockPallet node")

    def control_loop(self, event):
        if self.initial_position is None:
            self.initial_position = self.get_initial_pallet_position()
            if self.initial_position:
                rospy.loginfo(f"Pallet Initial Values {self.initial_position}")
        
        if self.initial_position:
            initial_x, initial_y = self.initial_position
            rospy.loginfo(f"Using initial position: x={initial_x}, y={initial_y}")

            # Intermediate position 2 units ahead in x direction
            intermediate_x = initial_x + 2
            intermediate_y = initial_y

            # Generate waypoints along a curve from initial to intermediate
            waypoints = self.generate_curve_waypoints(initial_x , initial_y, intermediate_x, intermediate_y)
            
            for waypoint in waypoints:
                rospy.loginfo(f"Waypoint: x={waypoint[0]}, y={waypoint[1]}")

            # Plot the curve
            self.plot_curve(initial_x, initial_y, waypoints, intermediate_x, intermediate_y)

    def update_tf_data(self):
        try:
            (pallet_trans, pallet_rot) = self.tf_listener.lookupTransform('/odom', '/pallet_center', rospy.Time(0))
            (fork_trans, fork_rot) = self.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.update_frame(pallet_trans, pallet_rot, fork_trans, fork_rot)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logwarn("LookupException: " + str(e))

    def update_frame(self, pallet_trans, pallet_rot, fork_trans, fork_rot):
        self.pallet_x = pallet_trans[0]
        self.pallet_y = pallet_trans[1]
        self.pallet_angle = self.euler_from_quaternion(pallet_rot)

        self.fork_x = fork_trans[0]
        self.fork_y = fork_trans[1]
        self.fork_angle = self.euler_from_quaternion(fork_rot)

    def euler_from_quaternion(self, quaternion):
        (roll, pitch, yaw) = tf.transformations.euler_from_quaternion(quaternion)
        return yaw
    
    def get_initial_pallet_position(self):
        try:
            (pallet_trans, pallet_rot) = self.tf_listener.lookupTransform('/odom', '/pallet_center', rospy.Time(0))
            self.get_initial_x = pallet_trans[0]
            self.get_initial_y = pallet_trans[1]

            rospy.loginfo(f"Initial Transform: x --> {self.get_initial_x} y --> {self.get_initial_y}")
            self.initial_position = (self.get_initial_x, self.get_initial_y)
            return self.initial_position

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logerr("Error occurred: %s", str(e))
            return None

    def generate_curve_waypoints(self, start_x, start_y, end_x, end_y, num_points=10):
        control_x = (start_x + end_x) / 2
        control_y = start_y + 1  # Control point to create a curved path

        t_values = np.linspace(0, 1, num_points)
        waypoints = []
        for t in t_values:
            x = (1 - t)**2 * start_x + 2 * (1 - t) * t * control_x + t**2 * end_x
            y = (1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * end_y
            waypoints.append((x, y))
        return waypoints

    def plot_curve(self, start_x, start_y, waypoints, end_x, end_y):
        waypoints_x = [point[0] for point in waypoints]
        waypoints_y = [point[1] for point in waypoints]

        plt.figure()
        plt.plot(waypoints_x, waypoints_y, label='Bezier Curve')
        plt.scatter([start_x, end_x], [start_y, end_y], color='red', label='Start/End Points')
        plt.title('Path from Fork to Intermediate Position')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == '__main__':
    try:
        dock_pallet = DockPallet()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Pallet docking terminated.")
