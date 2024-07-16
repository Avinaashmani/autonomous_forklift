#!/usr/bin/env python3

import rospy
import rosparam
import tf
import cv2
import numpy as np
from math import sqrt, atan2, pi
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

        self.threshold_distance = rosparam.get_param('/threshold_distance')
        self.threshold_angle = rosparam.get_param('threshold_angle')

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

        kp_angle_dynamic = dynamic_gain(self.kp_angle, path_angle, self.threshold_angle)
        kd_angle_dynamic = dynamic_gain(self.kd_angle, path_angle, self.threshold_angle)

        self.controlled_speed = (kp_distance_dynamic * distance + kd_distance_dynamic * diff_distance)
        self.controlled_angle = (kp_angle_dynamic * path_angle + kd_angle_dynamic * diff_angle)

        if abs(path_angle) < 0.02:
            self.controlled_angle = 0.0

        max_linear_speed = 0.1
        max_angular_speed = 0.6

        self.controlled_speed = round(abs(max(-max_linear_speed, min(max_linear_speed, self.controlled_speed))), 3)
        self.controlled_angle = round(abs(max(-max_angular_speed, min(max_angular_speed, self.controlled_angle))), 2)

        self.previous_distance = distance
        self.previous_angle = path_angle

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

        rospy.loginfo(f"Left Yaw: {self.left_} --Right Yaw: {self.right_} --Average: {self.average}")
        rospy.loginfo(f"Controlled Angle: {self.controlled_angle}")
        cv2.imshow('PID Tuning', np.zeros((1, 1), dtype=np.uint8))
        cv2.waitKey(1)

    def execute_phase_1(self):
        if self.path_angle_err < -pi/4 or self.path_angle_err > pi/4:
            if self.pallet_y < 0 and self.fork_y < self.pallet_y:
                self.path_angle_err = -2 * pi + self.path_angle_err
            elif self.pallet_y >= 0 and self.fork_y > self.pallet_y:
                self.path_angle_err = 2 * pi + self.path_angle_err

        if self.last_rotation > pi - 0.1 and self.rotation <= 0:
            self.rotation = 2 * pi + self.rotation
        elif self.last_rotation < -pi + 0.1 and self.rotation > 0:
            self.rotation = -2 * pi + self.rotation

        intermediate_x = (self.fork_x + self.pallet_x) / 2
        intermediate_y = (self.fork_y + self.pallet_y) / 2

        self.point_msg.positions = [self.controlled_angle]
        self.steering_msg.points = [self.point_msg]
        self.cmd_vel.linear.x = -self.controlled_speed

        self.move_cmd.publish(self.cmd_vel)
        self.steering_pub.publish(self.steering_msg)

    def execute_phase_2(self):
        rospy.loginfo("Phase 2")
        rospy.loginfo("Docking approach")

        if self.left_ < 0 and self.right_ < 0:
            if 0.0 < abs(self.average) < 0.05:
                self.point_msg.positions = [0.0]
                self.steering_msg.points = [self.point_msg]
                self.cmd_vel.linear.x = -0.1
                self.move_cmd.publish(self.cmd_vel)
                self.steering_pub.publish(self.steering_msg)
            else:
                self.point_msg.positions = [-self.controlled_angle]
                self.steering_msg.points = [self.point_msg]
                self.cmd_vel.linear.x = -self.controlled_speed
                self.move_cmd.publish(self.cmd_vel)
                self.steering_pub.publish(self.steering_msg)
        else:
            self.point_msg.positions = [self.controlled_angle]
            self.steering_msg.points = [self.point_msg]
            self.cmd_vel.linear.x = -self.controlled_speed
            self.move_cmd.publish(self.cmd_vel)
            self.steering_pub.publish(self.steering_msg)

    def execute_stop(self):
        rospy.loginfo("Reached")

        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        self.point_msg.positions = [0.0]
        self.steering_msg.points = [self.point_msg]
        
        self.move_cmd.publish(self.cmd_vel)
        self.steering_pub.publish(self.steering_msg)

    def update_tf_data(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform('/pallet', '/fork', rospy.Time(0))
            self.fork_x = trans[0]
            self.fork_y = trans[1]

            (pallet_trans, pallet_rot) = self.tf_listener.lookupTransform('/map', '/pallet', rospy.Time(0))
            self.pallet_x = pallet_trans[0]
            self.pallet_y = pallet_trans[1]

            self.rotation = tf.transformations.euler_from_quaternion(rot)[2] # type: ignore
            self.last_rotation = self.rotation

            self.distance = sqrt(self.fork_x ** 2 + self.fork_y ** 2)
            self.path_angle_err = atan2(self.fork_y, self.fork_x)

            if self.fork_y < 0:
                self.path_angle_err = -self.path_angle_err

            (left_roller_trans, left_roller_rot) = self.tf_listener.lookupTransform('/map', '/left_roller', rospy.Time(0))
            self.left_roller_x = left_roller_trans[0]
            self.left_roller_y = left_roller_trans[1]
            self.left_roller_angle = tf.transformations.euler_from_quaternion(left_roller_rot)[2]
            self.left_ = self.left_roller_angle

            (right_roller_trans, right_roller_rot) = self.tf_listener.lookupTransform('/map', '/right_roller', rospy.Time(0))
            self.right_roller_x = right_roller_trans[0]
            self.right_roller_y = right_roller_trans[1]
            self.right_roller_angle = tf.transformations.euler_from_quaternion(right_roller_rot)[2]
            self.right_ = self.right_roller_angle

            self.average = (self.left_ + self.right_) / 2.0

        except tf.Exception as e:
            rospy.logerr("Failed to get TF data: %s", e)

if __name__ == "__main__":
    try:
        DockPallet()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("DockPallet node terminated.")
