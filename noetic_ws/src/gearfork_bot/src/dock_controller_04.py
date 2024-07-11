#!/usr/bin/env python3

import rospy
import rosparam
import tf
import cv2
import numpy as np
from math import sqrt, atan2, pi, cos, sin
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class DockPallet:

    def __init__(self):
        rospy.init_node('pallet_dock', anonymous=True)
        rosparam.load_file('/home/avinaash/autonomous_forklift/noetic_ws/src/gearfork_bot/config/pallet_docking_prams.yaml')

        self.pallet_x = 0.0
        self.pallet_y = 0.0
        self.pallet_angle = 0.0

        self.pallet_right_x = 0.0
        self.pallet_right_y = 0.0
        self.pallet_right_angle = 0.0

        self.pallet_left_x = 0.0
        self.pallet_left_y = 0.0
        self.pallet_left_angle = 0.0

        self.fork_x = 0.0
        self.fork_y = 0.0
        self.fork_angle = 0.0

        self.left_roller_x = 0.0
        self.left_roller_y = 0.0
        self.left_roller_angle = 0.0

        self.right_roller_x = 0.0
        self.right_roller_y = 0.0
        self.right_roller_angle = 0.0

        self.left_ = 0.0
        self.right_= 0.0
        self.average = 0.0

        self.distance = 0.0
        self.yaw_diff = 0.0
        self.path_angle_err = 0.0
        self.path_angle = 0.0

        self.move_cmd = rospy.Publisher('/gearfork_bot/cmd_vel', Twist, queue_size=10)
        self.steering_pub = rospy.Publisher('/gearfork_bot/steering_joint_controller/command', JointTrajectory, queue_size=10)
        self.tf_listener = tf.TransformListener()

        self.previous_distance = 0.0
        self.controlled_speed = 0.0
        self.previous_angle = 0.0
        self.controlled_angle = 0.0
        self.total_distance = 0.0
        self.total_angle = 0.0

        self.last_rotation = 0.0
        self.rotation = 0.0

        self.threshold_distance = 0.2
        self.threshold_angle = 0.05

        self.cmd_vel = Twist()
        self.steering_msg = JointTrajectory()
        self.point_msg = JointTrajectoryPoint()

        self.kp_distance = rosparam.get_param('/kp_distance')
        self.ki_distance = rosparam.get_param('/ki_distance')
        self.kd_distance = rosparam.get_param('/kd_distance')

        self.kp_angle = rosparam.get_param('/kp_angle')
        self.ki_angle = rosparam.get_param('/ki_angle')
        self.kd_angle = rosparam.get_param('/kd_angle')

        self.integral_distance = 0.0
        self.integral_angle = 0.0

        self.phase_1 = False
        self.phase_2 = False
        self.stop = False
        
        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.control_loop)

    def control_loop(self, event):
        self.update_tf_data()

        self.steering_msg.header.stamp = rospy.Time.now()
        self.steering_msg.header.frame_id = ''
        self.steering_msg.joint_names = ['motor_joint']

        self.point_msg.velocities = []
        self.point_msg.accelerations = []
        self.point_msg.effort = []

        diff_angle = self.previous_angle - self.path_angle
        diff_distance = self.previous_distance - self.distance
        
        control_signal_distance = self.kp_distance * self.distance + self.ki_distance * self.total_distance + self.kd_distance * diff_distance
        control_signal_angle = self.kp_angle * self.path_angle_err + self.ki_angle * self.total_angle + self.kd_angle * diff_angle
        
        self.controlled_speed = control_signal_distance
        self.controlled_angle = control_signal_angle
        
        rospy.loginfo(f"Angle: {self.controlled_angle}, Distance: {self.controlled_speed}")

        self.cmd_vel.linear.x = -abs(max(-0.2, min(0.2, self.controlled_speed)))
        self.cmd_vel.angular.z = max(-1.0, min(1.0, self.controlled_angle)) / 1000

        self.move_cmd.publish(self.cmd_vel)

        self.previous_distance = self.distance
        self.previous_angle = self.path_angle

    def update_tf_data(self):
        try:
            (trans_pallet, rot_pallet) = self.tf_listener.lookupTransform('/odom', '/pallet_center', rospy.Time(0))
            self.pallet_x = trans_pallet[0]
            self.pallet_y = trans_pallet[1]
            self.pallet_angle = euler_from_quaternion(rot_pallet)

            (trans_fork, rot_fork) = self.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.fork_x = trans_fork[0]
            self.fork_y = trans_fork[1]
            self.fork_angle = euler_from_quaternion(rot_fork)

            self.distance = sqrt((self.fork_x - self.pallet_x) ** 2 + (self.fork_y - self.pallet_y) ** 2)
            self.path_angle = atan2(self.pallet_y - self.fork_y, self.pallet_x - self.fork_x)
            self.path_angle_err = self.path_angle - self.fork_angle[2]

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("Failed to get TF data. Retrying...")

if __name__ == '__main__':
    try:
        DockPallet()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
