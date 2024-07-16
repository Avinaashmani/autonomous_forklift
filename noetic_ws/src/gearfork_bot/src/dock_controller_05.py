#!/usr/bin/env python3

import rospy
import rosparam
import tf
import time
from math import sqrt, atan2, pi, cos, sin
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist, Point
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

        self.distance = 0.0
        self.path_angle_err = 0.0

        self.intermediate_distance = 0.0
        self.intermediate_path_angle = 0.0

        self.controlled_angle = 0.0
        self.controlled_speed = 0.0

        self.move_cmd = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.steering_pub = rospy.Publisher('/gearfork_bot/steering_joint_controller/command', JointTrajectory, queue_size=10)
        self.tf_listener = tf.TransformListener()

        self.waypoints = []
        self.current_waypoint_index = 0
        self.waypoint_threshold = 0.2
        self.path_angle = 0.0

        self.cmd_vel = Twist()
        self.steering_msg = JointTrajectory()
        self.point_msg = JointTrajectoryPoint()

        self.kp_dist = 0.2
        self.kd_dist = 0.5

        self.kp_angle = 1.5
        self.kd_angle = 0.5

        self.quad_value = 0

        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.control_loop) # type: ignore
        rospy.on_shutdown(self.on_shutdown)

    def control_loop(self, event):
        self.update_tf_data()
        quadrant = self.check_orientation()
        print(quadrant)
        
        # if abs(self.fork_y) > 1.0:

        #     if quadrant == 1:
        #         self.quad_a()

        #     elif quadrant == 2:
        #         self.quad_b()

        # if abs(self.fork_y) < 1.0:
        self.dock()
        
    def check_orientation(self):
        
        distance_ = self.fork_y
        angle_ = self.fork_angle
        
        if 0 <= abs(angle_) <= 1.8:
            if distance_ > 0:
                self.quad_value = 1
            elif distance_ < 0:
                self.quad_value = 2
        
        if 1.8 <= abs(angle_) <= 3.14:
            if distance_ > 0:
                self.quad_value = 3

            elif distance_ < 0:
                self.quad_value = 4
        
        return self.quad_value

    def quad_a(self):
        rospy.loginfo("In Quadrant A")

        self.update_tf_data()

        distance_y = abs(self.fork_y)
        angle_ = abs(self.fork_angle)
        distance_ = abs(self.distance)

        if not hasattr(self, 'state'):
            self.state = 'align'

        if self.state == 'align':
            # Align the robot's angle between 1.4 and 1.7 radians
            if not (1.4 <= angle_ <= 1.7) and distance_y > 1.0:
                rospy.loginfo("Aligning angle")
                self.cmd_vel.linear.x = -0.3
                if self.fork_angle > 0:
                    self.cmd_vel.angular.z = -((1.45 - angle_) * self.kp_angle)
                else:
                    self.cmd_vel.angular.z = ((1.45 - angle_) * self.kp_angle)
                self.move_cmd.publish(self.cmd_vel)

            else:
                rospy.loginfo("Angle aligned, stopping to reset steering")
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = 0.0
                self.move_cmd.publish(self.cmd_vel)
                rospy.sleep(2)  # Wait for steering to return to zero position
                self.state = 'move_forward'

        elif self.state == 'move_forward':

            self.cmd_vel.angular.z = 0.0
            self.move_cmd.publish(self.cmd_vel)

            time.sleep(0.7)

            if abs(self.fork_y) > 1.0:
                rospy.loginfo("Moving forward")
                self.cmd_vel.linear.x = -0.3
                self.cmd_vel.angular.z = 0.0
                self.move_cmd.publish(self.cmd_vel)

            else:
                time.sleep(3)
                rospy.loginfo("Target reached, stopping")
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = 0.0
                self.move_cmd.publish(self.cmd_vel)
                self.state = 'stop'

        elif self.state == 'stop':
            time.sleep(3)
            rospy.loginfo("Docking process complete")
            self.cmd_vel.linear.x = 0.0
            self.cmd_vel.angular.z = 0.0
            self.move_cmd.publish(self.cmd_vel)

    def quad_b(self):
        rospy.loginfo("In Quadrant B")

        self.update_tf_data()

        distance_y = abs(self.fork_y)
        angle_ = abs(self.fork_angle)
        distance_ = abs(self.distance)

        if not hasattr(self, 'b_state'):
            self.b_state = 'check'

        if self.b_state == 'check':
            if abs(self.fork_y) > 1.0:
                self.b_state = 'align'

            elif abs(self.fork_y) < 1.0:
                self.b_state = 'dock'

        elif self.b_state == 'align':

            if not (1.4 <= angle_ <= 1.7) and distance_y > 1.0:
                rospy.loginfo("Aligning angle")
                self.cmd_vel.linear.x = -0.3
                
                if self.fork_angle > 0:
                    self.cmd_vel.angular.z = -((1.45 - angle_) * self.kp_angle)
                
                else:
                    self.cmd_vel.angular.z = ((1.45 - angle_) * self.kp_angle)
                self.move_cmd.publish(self.cmd_vel)

            else:
                rospy.loginfo("Angle aligned, stopping to reset steering")
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = 0.0
                self.move_cmd.publish(self.cmd_vel)
                rospy.sleep(2) 
                self.b_state = 'move_forward'

        elif self.b_state == 'move_forward':

            self.cmd_vel.angular.z = 0.0
            self.move_cmd.publish(self.cmd_vel)
            time.sleep(0.7)

            if abs(self.fork_y) > 1.0:
                rospy.loginfo("Moving forward")
                self.cmd_vel.linear.x = -0.3
                self.cmd_vel.angular.z = 0.0
                self.move_cmd.publish(self.cmd_vel)
            
            else:
                time.sleep(3)
                rospy.loginfo("Target reached, stopping")
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = 0.0
                self.move_cmd.publish(self.cmd_vel)
                self.b_state = 'dock'

        elif self.b_state == 'dock':

            if self.dock():
                self.b_state = 'stop'

            else:
                self.b_state = 'check_error'

        elif self.b_state == 'stop':
            time.sleep(3)
            rospy.loginfo("Docking process complete")
            self.cmd_vel.linear.x = 0.0
            self.cmd_vel.angular.z = 0.0
            self.move_cmd.publish(self.cmd_vel)

        elif self.b_state == 'check_error':
            rospy.logerr("Error in Quadradent B Docking, Please Check")

    def dock(self):
        self.update_tf_data()

        distance_y = self.fork_y  
        angle_ = self.fork_angle  
        distance_ = self.pallet_x  

        kp_dist = angle_ 
        kd_dist = 1.0
        
        kp_angle = distance_y /5
        kd_angle = 0.05
        
        if not hasattr(self, 'docking_state'):
            self.docking_state = 'align'

        if not hasattr(self, 'prev_error_dist'):
            self.prev_error_dist = 0
        
        if not hasattr(self, 'prev_error_angle'):
            self.prev_error_angle = 0

        error_dist = distance_
        derivative_dist = (error_dist - self.prev_error_dist)

        error_angle = angle_ - distance_y
        derivative_angle = (error_angle - self.prev_error_angle) / 0.1

        controlled_speed = abs(round(kp_dist * error_dist + kd_dist * derivative_dist, 3))
        controlled_angle = round(kp_angle * error_angle + kd_angle * derivative_angle, 4)

        rospy.loginfo(f"Fork Y: {distance_y} Speed: {distance_y * 0.5}")
        rospy.loginfo(f"Angle: {controlled_angle}")
        rospy.loginfo(f"Speed {controlled_speed * 10}")
        
        if self.docking_state == 'align':

            if abs(distance_y) > 0.098:
                
                if distance_y > 0:
                    self.cmd_vel.linear.x = -controlled_speed  
                    self.cmd_vel.angular.z += controlled_angle  
                    self.move_cmd.publish(self.cmd_vel)

                elif distance_y < 0:                                             
                    self.cmd_vel.linear.x = -controlled_speed  
                    self.cmd_vel.angular.z -= controlled_angle  
                    self.move_cmd.publish(self.cmd_vel)                      

                # self.move_cmd.publish(self.cmd_vel)

            elif distance_y < 0.03:

                self.docking_state = 'move_forward'

        elif self.docking_state == 'move_forward':
            self.cmd_vel.angular.z = 0.0
            self.move_cmd.publish(self.cmd_vel)

            if abs(distance_) > 0.5:
                rospy.loginfo("Moving forward")

                self.cmd_vel.linear.x = -0.2
                if not 0.0 <= abs(self.fork_angle) <= 0.05:
                    # if angle_ > 0:
                    #     self.cmd_vel.angular.z = controlled_angle

                    # elif angle_ < 0:
                    #     self.cmd_vel.angular.z = controlled_angle
                    # self.move_cmd.publish(self.cmd_vel)

                    self.cmd_vel.angular.z = controlled_angle *  10
                    self.move_cmd.publish(self.cmd_vel)

                else:
                    self.cmd_vel.angular.z = 0.0
                    self.move_cmd.publish(self.cmd_vel)
            else:
                rospy.loginfo("Target reached, stopping")
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = 0.0
                self.move_cmd.publish(self.cmd_vel)
                self.docking_state = 'stop'

        elif self.docking_state == 'stop':
            rospy.loginfo("Docking State: Stop")
            self.cmd_vel.linear.x = 0.0
            self.cmd_vel.angular.z = 0.0
            self.move_cmd.publish(self.cmd_vel)

        self.prev_error_dist = error_dist
        self.prev_error_angle = error_angle

    def on_shutdown(self):
        rospy.loginfo("Shutting down DockPallet node")
        self.control_timer.shutdown()

        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        self.move_cmd.publish(self.cmd_vel)

        rospy.loginfo("DockPallet node shutdown complete")

    def update_tf_data(self):
        try:
            (trans_pallet, rot_pallet) = self.tf_listener.lookupTransform('/base_link', '/pallet_center', rospy.Time(0))
            self.pallet_x = round(trans_pallet[0], 3)
            self.pallet_y = round(trans_pallet[1], 3)
            self.pallet_angle = round(euler_from_quaternion(rot_pallet)[2], 3)

            (trans_fork, rot_fork) = self.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.fork_x = round(trans_fork[0], 3)
            self.fork_y = round(trans_fork[1], 3)
            self.fork_angle = round(euler_from_quaternion(rot_fork)[2], 3)

            self.distance = sqrt((self.pallet_x - self.fork_x) ** 2 + (self.pallet_y - self.fork_y) ** 2)
            self.intermediate_distance = sqrt(((self.pallet_x + 3.0) - self.fork_x) ** 2 + (self.pallet_y - self.fork_y) ** 2)

            self.path_angle_err = abs(atan2(self.fork_y - self.pallet_y, self.fork_x - self.pallet_x)) - self.fork_angle
            self.intermediate_path_angle = atan2(self.pallet_y - self.fork_y, self.pallet_x - self.fork_x) - self.fork_angle

            # rospy.loginfo(f"TF Data - Fork X: {self.fork_x}, Y: {self.fork_y}, Angle: {self.fork_angle}")
            # rospy.loginfo(f"TF Data - Pallet X: {self.pallet_x}, Y: {self.pallet_y}, Angle: {self.pallet_angle}")
            # rospy.loginfo(f"Distance to Pallet: {self.distance}")

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("Failed to get TF data. Retrying...")

if __name__ == '__main__':
    try:
        DockPallet()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
