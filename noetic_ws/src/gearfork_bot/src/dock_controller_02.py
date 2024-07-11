#!/usr/bin/env python3

import rospy
import rosparam
import tf
import cv2
import numpy as np
from math import sqrt, atan2, pi, cos, sin
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
        rospy.loginfo("Initialized DockPallet node")

    def create_trackbars(self):
        cv2.namedWindow('PID Tuning')

        cv2.createTrackbar('Kp Distance', 'PID Tuning', int(self.kp_distance * 100), 1000, self.nothing)
        cv2.createTrackbar('Kd Distance', 'PID Tuning', int(self.kd_distance * 100), 1000, self.nothing)
        
        cv2.createTrackbar('Kp Angle', 'PID Tuning', int(self.kp_angle * 100), 1000, self.nothing)
        cv2.createTrackbar('Kd Angle', 'PID Tuning', int(self.kd_angle * 100), 1000, self.nothing)

        cv2.imshow('PID Tuning', np.zeros((1,1), dtype=np.uint8))
        cv2.waitKey(1)

    def update_pid_from_trackbars(self):
        self.kp_distance = cv2.getTrackbarPos('Kp Distance', 'PID Tuning') / 100.0
        self.kd_distance = cv2.getTrackbarPos('Kd Distance', 'PID Tuning') / 100.0
        
        self.kp_angle = cv2.getTrackbarPos('Kp Angle', 'PID Tuning') / 100.0
        self.kd_angle = cv2.getTrackbarPos('Kd Angle', 'PID Tuning') / 100.0

    def nothing(self, x):
        pass

    def control_loop(self, event):
        self.create_trackbars()
        self.update_pid_from_trackbars()
        self.update_tf_data()

        self.steering_msg.header.stamp = rospy.Time.now()
        self.steering_msg.header.frame_id = ''
        self.steering_msg.joint_names = ['motor_joint']

        self.point_msg.velocities = []
        self.point_msg.accelerations = []
        self.point_msg.effort = []

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

        kp_angle_dynamic = dynamic_gain(self.kp_angle, self.average, self.threshold_angle)
        kd_angle_dynamic = dynamic_gain(self.kd_angle, self.average, self.threshold_angle)

        self.controlled_speed = (kp_distance_dynamic * distance + kd_distance_dynamic * diff_distance)
        self.controlled_angle = (kp_angle_dynamic * self.average + kd_angle_dynamic * diff_angle)

        if abs(path_angle) < 0.02:
            self.controlled_angle = 0.0

        max_linear_speed = 0.1
        max_angular_speed = 2.0

        self.controlled_speed = max(-max_linear_speed, min(max_linear_speed, self.controlled_speed))
        self.controlled_angle = max(-max_angular_speed, min(max_angular_speed, self.controlled_angle))

        self.previous_distance = distance
        self.previous_angle = path_angle

        rospy.loginfo(f"Distance: {distance:.2f}, Path Angle Error: {path_angle:.2f}")
        # rospy.loginfo(f"Controlled Speed: {self.controlled_speed:.2f}, Controlled Angle: {self.controlled_angle * 10:.2f}, PathAngle: {path_angle:.2f}")

        if distance > 2.5:
            self.phase_1 = True
            self.phase_2 = False
            self.stop = False
        elif 0.5 < distance < 2.5:
            self.phase_1 = False
            self.phase_2 = True 
            self.stop = False
        else:
            self.phase_1 = False
            self.phase_2 = False
            self.stop = True

        if self.phase_1:
            self.execute_phase_1()

        if self.phase_2:
            self.execute_phase_2()

        if self.stop:
            self.execute_stop()

        rospy.loginfo(f"Left Yaw: {self.left_} -- Right Yaw: {self.right_} -- Average: {self.average}")
        cv2.imshow('PID Tuning', np.zeros((1, 1), dtype=np.uint8))
        cv2.waitKey(1)

    def execute_phase_1(self):
        rospy.loginfo("Executing Phase 1: Aligning with the center of the pallet")

        # if self.path_angle_err < -pi/4 or self.path_angle_err > pi/4:

        #     if self.pallet_y < 0 and self.fork_y < self.pallet_y:
        #         self.path_angle_err = -2 * pi + self.path_angle_err

        #     elif self.pallet_y >= 0 and self.fork_y > self.pallet_y:
        #         self.path_angle_err = 2 * pi + self.path_angle_err

        if self.last_rotation > pi - 0.1 and self.fork_angle <= 0:
            self.fork_angle = 2 * pi + self.fork_angle

        elif self.last_rotation < -pi + 0.1 and self.fork_angle > 0:
            self.fork_angle = -2 * pi + self.fork_angle

        # Calculate intermediate point 2 meters away from the pallet center
        intermediate_distance = 2.0
        intermediate_x = self.pallet_x  + intermediate_distance
        intermediate_y = self.pallet_y  

        # Update the path angle and distance to the intermediate point
        path_angle_to_intermediate = atan2(intermediate_y - self.fork_y, intermediate_x - self.fork_x)
        distance_to_intermediate = sqrt((intermediate_x - self.fork_x) ** 2 + (intermediate_y - self.fork_y) ** 2)

        rospy.loginfo(f"Intermediate Target: ({intermediate_x}, {intermediate_y}), Distance: {distance_to_intermediate:.2f}, Path Angle: {path_angle_to_intermediate * 2:.2f}")
        rospy.loginfo(f"Controlled Speed: {self.controlled_speed:.2f}, Controlled Angle: {self.controlled_angle * 10:.2f}, PathAngle: {path_angle_to_intermediate:.2f}")
        
        rospy.loginfo(f"Rotation --> {self.fork_angle}")

        # Calculate controlled angle for alignment
        self.controlled_angle = path_angle_to_intermediate - self.fork_angle

        # Cap the control inputs to ensure smooth motion
        max_angular_speed = 1.0
        self.controlled_angle = max(-max_angular_speed, min(max_angular_speed, self.controlled_angle))

        self.point_msg.positions = [self.controlled_angle]
        self.steering_msg.points = [self.point_msg]

        self.steering_pub.publish(self.steering_msg)
        self.cmd_vel.linear.x = -0.2

        self.move_cmd.publish(self.cmd_vel)

        self.last_rotation = self.fork_angle

    def execute_phase_2(self):
        rospy.loginfo("Executing Phase 2: Aligning to center of the pallet")

        # Calculate the distance and path angle to the pallet center
        distance_to_pallet = sqrt((self.pallet_x - self.fork_x) ** 2 + (self.pallet_y - self.fork_y) ** 2)
        path_angle_to_pallet = atan2(self.pallet_y - self.fork_y, self.pallet_x - self.fork_x)

        rospy.loginfo(f"Pallet Target: ({self.pallet_x}, {self.pallet_y}), Distance: {distance_to_pallet:.2f}, Path Angle: {path_angle_to_pallet:.2f}")

        # Calculate controlled angle and speed for alignment
        self.controlled_angle = path_angle_to_pallet - self.fork_angle

        # Cap the control inputs to ensure smooth motion
        max_linear_speed = 0.05
        max_angular_speed = 1.0

        self.controlled_speed = max(-max_linear_speed, min(max_linear_speed, self.controlled_speed))
        self.controlled_angle = max(-max_angular_speed, min(max_angular_speed, self.controlled_angle))

        self.cmd_vel.linear.x = -0.2

        self.move_cmd.publish(self.cmd_vel)

    def execute_stop(self):
        rospy.loginfo("Stopping the robot")

        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0

        self.move_cmd.publish(self.cmd_vel)

    def update_tf_data(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform('/odom', '/pallet_center', rospy.Time(0))
            self.pallet_x = trans[0]
            self.pallet_y = trans[1]
            self.pallet_angle = atan2(self.pallet_y, self.pallet_x)

            (trans, rot) = self.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.fork_x = trans[0]
            self.fork_y = trans[1]
            self.fork_angle = atan2(self.fork_y, self.fork_x)

            (trans, rot) = self.tf_listener.lookupTransform('/base_link', '/lroller_link', rospy.Time(0))
            self.left_roller_x = trans[0]
            self.left_roller_y = trans[1]
            self.left_roller_angle = atan2(self.left_roller_y, self.left_roller_x)

            (trans, rot) = self.tf_listener.lookupTransform('/base_link', '/rroller_link', rospy.Time(0))
            self.right_roller_x = trans[0]
            self.right_roller_y = trans[1]
            self.right_roller_angle = atan2(self.right_roller_y, self.right_roller_x)

            self.left_ = self.left_roller_angle
            self.right_ = self.right_roller_angle

            self.average = (self.left_ + self.right_) / 2

            self.distance = sqrt((self.pallet_x - self.fork_x) ** 2 + (self.pallet_y - self.fork_y) ** 2)
            self.yaw_diff = abs(self.fork_angle - self.pallet_angle)

            path_angle_to_pallet = atan2(self.pallet_y - self.fork_y, self.pallet_x - self.fork_x)
            self.path_angle_err = path_angle_to_pallet - self.fork_angle

            rospy.loginfo(f"Pallet Position: ({self.pallet_x}, {self.pallet_y}), Angle: {self.pallet_angle:.2f}")
            rospy.loginfo(f"Fork Position: ({self.fork_x}, {self.fork_y}), Angle: {self.fork_angle:.2f}")

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("Failed to get TF data. Retrying...")

if __name__ == '__main__':
    try:
        DockPallet()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass