#!/usr/bin/env python3

import rospy
import math
import tf
import cv2
import numpy as np
from math import sqrt, atan2, pi, asin
from geometry_msgs.msg import Twist

class Dockpallet:

    def __init__(self):
        rospy.init_node('pallet_dock', anonymous=True)
        rospy.loginfo_once('Dock with Pallet using test setup....')

        self.pallet_x = 0.0
        self.pallet_y = 0.0
        self.pallet_angle = 0.0

        self.tb3_x = 0.0
        self.tb3_y = 0.0
        self.tb3_angle = 0.0

        self.distance = 0.0
        self.yaw_diff = 0.0
        self.path_angle_err = 0.0

        self.move_cmd = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.tf_listener = tf.TransformListener()

        self.previous_distance = 0.0
        self.controlled_speed = 0.0
        self.previous_angle = 0.0
        self.controlled_angle = 0.0

        self.threshold_distance = 0.5
        self.threshold_angle = 0.02

        self.cmd_vel = Twist()

        self.kp_distance = 0.1
        self.ki_distance = 0.0
        self.kd_distance = 0.1

        self.kp_angle = 0.55
        self.ki_angle = 0.0
        self.kd_angle = 30.0

        self.integral_distance = 0.0
        self.integral_angle = 0.0

        self.phase_1 = False
        
        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.control_loop)
        rospy.loginfo("Initialized Dockpallet node")

    def create_trackbars(self):
        cv2.namedWindow('PID Tuning')

        cv2.createTrackbar('Kp Distance', 'PID Tuning', int(self.kp_distance * 100), 1000, self.nothing)
        # cv2.createTrackbar('Ki Distance', 'PID Tuning', int(self.ki_distance * 100), 1000, self.nothing)
        cv2.createTrackbar('Kd Distance', 'PID Tuning', int(self.kd_distance * 100), 1000, self.nothing)
        cv2.createTrackbar('Kp Angle', 'PID Tuning', int(self.kp_angle * 100), 1000, self.nothing)
        # cv2.createTrackbar('Ki Angle', 'PID Tuning', int(self.ki_angle * 100), 1000, self.nothing)
        cv2.createTrackbar('Kd Angle', 'PID Tuning', int(self.kd_angle * 100), 1000, self.nothing)

        cv2.imshow('PID Tuning', np.zeros((1,1), dtype=np.uint8))
        cv2.waitKey(1)

    def update_pid_from_trackbars(self):
        self.kp_distance = cv2.getTrackbarPos('Kp Distance', 'PID Tuning') / 100.0
        # self.ki_distance = cv2.getTrackbarPos('Ki Distance', 'PID Tuning') / 100.0
        self.kd_distance = cv2.getTrackbarPos('Kd Distance', 'PID Tuning') / 100.0
        self.kp_angle = cv2.getTrackbarPos('Kp Angle', 'PID Tuning') / 100.0
        # self.ki_angle = cv2.getTrackbarPos('Ki Angle', 'PID Tuning') / 100.0
        self.kd_angle = cv2.getTrackbarPos('Kd Angle', 'PID Tuning') / 100.0

    def nothing(self, x):
        try:
            pass
        except TypeError:
            pass

    def control_loop(self, event):
        self.create_trackbars()
        self.update_pid_from_trackbars()
        self.update_tf_data()

        distance = self.distance
        path_angle = self.path_angle_err

        self.integral_distance += distance
        self.integral_angle += path_angle

        diff_angle = path_angle - self.previous_angle
        diff_distance = distance - self.previous_distance

        def dynamic_gain(base_gain, error, threshold):
            if abs(error) < threshold:
                return base_gain * (1 + (threshold - abs(error)) / threshold)
            else:
                return base_gain * threshold / abs(error)

        kp_distance_dynamic = dynamic_gain(self.kp_distance, distance, self.threshold_distance)
        kd_distance_dynamic = dynamic_gain(self.kd_distance, distance, self.threshold_distance)

        kp_angle_dynamic = dynamic_gain(self.kp_angle, path_angle, self.threshold_angle)
        kd_angle_dynamic = dynamic_gain(self.kd_angle, path_angle, self.threshold_angle)

        self.controlled_speed = (kp_distance_dynamic * distance + kd_distance_dynamic * diff_distance)
        self.controlled_angle = (kp_angle_dynamic * path_angle + kd_angle_dynamic * diff_angle)

        if abs(path_angle) < 0.02:
            self.controlled_angle = 0.0

        max_linear_speed = 0.1
        max_angular_speed = 0.10

        self.controlled_speed = max(-max_linear_speed, min(max_linear_speed, self.controlled_speed))
        self.controlled_angle = max(-max_angular_speed, min(max_angular_speed, self.controlled_angle))

        self.cmd_vel.angular.z = self.controlled_angle
        self.cmd_vel.linear.x = -self.controlled_speed
        self.move_cmd.publish(self.cmd_vel)

        rospy.loginfo(f"Control loop: Distance = {distance:.2f}, Path angle = {path_angle:.2f}, Controlled speed = {self.controlled_speed:.2f}, Controlled angle = {self.controlled_angle:.2f}")

        self.previous_distance = distance
        self.previous_angle = path_angle

        if distance > 0.5:
            rospy.loginfo("Docking approach")

            if 0 < abs(self.yaw_diff) <= 0.5:
                self.controlled_angle = 0.0
                self.controlled_speed = 0.0

                self.cmd_vel.angular.z = 0.0
                self.cmd_vel.linear.x = -0.1

                self.move_cmd.publish(self.cmd_vel)
                rospy.loginfo("In the correct angle Range")

            else:
                if self.yaw_diff > 0.6:
                    self.cmd_vel.angular.z = -0.2
                    self.cmd_vel.linear.x = 0.0

                    self.move_cmd.publish(self.cmd_vel)
                    rospy.loginfo("Phase 1: Adjusting to the right")
                elif self.yaw_diff < -0.6:
                    self.cmd_vel.angular.z = 0.2
                    self.cmd_vel.linear.x = 0.0

                    self.move_cmd.publish(self.cmd_vel)
                    rospy.loginfo("Phase 1: Adjusting to the left")

        elif distance < 0.5:
            self.cmd_vel.angular.z = 0.0
            self.cmd_vel.linear.x = 0.0

            self.move_cmd.publish(self.cmd_vel)

        cv2.imshow('PID Tuning', np.zeros((1, 1), dtype=np.uint8))
        cv2.waitKey(1)

    def update_tf_data(self):
        try:
            (pallet_trans, pallet_rot) = self.tf_listener.lookupTransform('/odom', '/pallet_center', rospy.Time(0))
            (tb3_trans, tb3_rot) = self.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.update_frame(pallet_trans, pallet_rot, tb3_trans, tb3_rot)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logwarn("LookupException: " + str(e))

    def update_frame(self, pallet_trans, pallet_rot, tb3_trans, tb3_rot):
        self.pallet_x = pallet_trans[0]
        self.pallet_y = pallet_trans[1]
        self.pallet_angle = self.euler_from_quaternion(pallet_rot)

        self.tb3_x = tb3_trans[0]
        self.tb3_y = tb3_trans[1]
        self.tb3_angle = self.euler_from_quaternion(tb3_rot)

        self.distance = sqrt(pow(self.pallet_x - self.tb3_x, 2) + pow(self.pallet_y - self.tb3_y, 2))
        self.path_angle_err = atan2(self.pallet_y - self.tb3_y, self.pallet_x - self.tb3_x) / pi

        self.yaw_diff = self.path_angle_err

        angle_err_pallet = atan2(self.pallet_y, self.pallet_x)
        angle_err_robot = atan2(self.tb3_y, self.tb3_x)

        self.distance = self.distance
        self.yaw_diff = self.path_angle_err - self.tb3_angle
        self.path_angle_err = angle_err_pallet - angle_err_robot

        rospy.loginfo(f"TF Update: Pallet (x, y, angle) = ({self.pallet_x:.2f}, {self.pallet_y:.2f}, {self.pallet_angle:.2f}), "
                      f"Robot (x, y, angle) = ({self.tb3_x:.2f}, {self.tb3_y:.2f}, {self.tb3_angle:.2f}), "
                      f"Distance = {self.distance:.2f}, Yaw diff = {self.yaw_diff:.2f}, Path angle error = {self.path_angle_err:.2f}")

    def euler_from_quaternion(self, quaternion):
        (roll, pitch, yaw) = tf.transformations.euler_from_quaternion(quaternion)
        return yaw

if __name__ == '__main__':
    try:
        dock_pallet = Dockpallet()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Pallet docking terminated.")
