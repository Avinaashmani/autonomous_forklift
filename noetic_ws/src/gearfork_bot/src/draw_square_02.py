#!/usr/bin/env python3

import rospy
import tf
import py_trees

from math import sqrt, atan2, pi
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist, TransformStamped
import tf2_ros

class TransferData:
    def __init__(self):
        self.linear_x = 0.0
        self.angular_z = 0.0

class DrawSquare:
    def __init__(self):
        rospy.init_node("draw_square_01", anonymous=True)
        rospy.loginfo("Draw Square Node started...")
        self.tf_listener = tf.TransformListener()
        self.move_cmd = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.behaviour_tree = self.create_behaviour_tree()
        
    def create_behaviour_tree(self):
        root = py_trees.composites.Sequence("Root")

        move_to_point_1 = MoveToPoint(self, target_frame="point_1")
        turn_90_1 = Turn90Degrees(self, target_frame="point_2")

        move_to_point_2 = MoveToPoint(self, target_frame="point_2")
        turn_90_2 = Turn90Degrees(self, target_frame="point_3")

        move_to_point_3 = MoveToPoint(self, target_frame="point_3")
        turn_90_3 = Turn90Degrees(self, target_frame="starting_point")
        
        move_to_point_4 = MoveToPoint(self, target_frame="starting_point")
        turn_90_4 = Turn90Degrees(self, target_frame="point_1")

        root.add_children([move_to_point_1, turn_90_1, move_to_point_2, turn_90_2, move_to_point_3, turn_90_3, move_to_point_4, turn_90_4])
        return py_trees.trees.BehaviourTree(root)
    
    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.behaviour_tree.tick()
            rate.sleep()

class MoveToPoint(py_trees.behaviour.Behaviour):
    def __init__(self, draw_square, target_frame):
        super(MoveToPoint, self).__init__(name=f"Move to {target_frame}")
        rospy.loginfo(f"Move to {target_frame}")
        self.draw_square = draw_square
        self.target_frame = target_frame
        self.cmd_vel = Twist()
        self.update()
        self.start_time = rospy.get_time()

    def update(self):
        
        if self.update_tf_data():
            rospy.loginfo(self.distance)
            if abs(self.distance) < 0.1:
                self.stop_robot()
                return py_trees.common.Status.SUCCESS
            else:
                self.cmd_vel.linear.x = 0.2
                self.cmd_vel.angular.z = 0.05 * self.path_angle_err
                self.draw_square.move_cmd.publish(self.cmd_vel)
                rospy.loginfo(f"Publishing cmd_vel: linear.x={self.cmd_vel.linear.x}, angular.z={self.cmd_vel.angular.z}")
                return py_trees.common.Status.RUNNING
        else:
            return py_trees.common.Status.RUNNING

    def update_tf_data(self):
        try:
            (trans_target, rot_target) = self.draw_square.tf_listener.lookupTransform('/base_link', self.target_frame, rospy.Time(0))
            self.point_x = trans_target[0]
            self.point_y = trans_target[1]
            self.point_angle_z = euler_from_quaternion(rot_target)[2]

            (trans_fork, rot_fork) = self.draw_square.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.fork_x = trans_fork[0]
            self.fork_y = trans_fork[1]
            self.fork_angle_z = euler_from_quaternion(rot_fork)[2]

            self.distance = sqrt((self.point_x - self.fork_x) ** 2 + (self.point_y - self.fork_y) ** 2)
            self.path_angle_err = atan2(self.point_y - self.fork_y, self.point_x - self.fork_x) - self.fork_angle_z
            
            return True

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logwarn(f"Failed to get TF data: {e}")
            return False

    def stop_robot(self):
        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        self.draw_square.move_cmd.publish(self.cmd_vel)
        rospy.loginfo("Stopping robot")

class Turn90Degrees(py_trees.behaviour.Behaviour):
    
    def __init__(self, draw_square, target_frame):
        super(Turn90Degrees, self).__init__(name="Turn 90 Degrees")
        self.draw_square = draw_square
        self.cmd_vel = Twist()
        self.update()
        self.start_time = rospy.get_time()
        self.target_frame = target_frame

        self.point_x = 0.0
        self.point_y = 0.0
        self.point_angle_z = 0.0

        self.fork_x = 0.0
        self.fork_y = 0.0
        self.fork_angle_z

        self.path_angle_err = 0.0
        self.distance = 0.0
    
    def initialise(self):
        self.start_time = rospy.get_time()
        
    def update(self):
        self.update_tf_data()
        self.start_time = rospy.get_time()
        elapsed_time = rospy.get_time() - self.start_time
        
        if elapsed_time < 2.0:  
            self.cmd_vel.angular.z = 0.0  
            self.cmd_vel.linear.x = 0.0
            self.draw_square.move_cmd.publish(self.cmd_vel)
            rospy.loginfo(f"Turning: ={self.fork_angle_z}")
            return py_trees.common.Status.SUCCESS
        
        else:
            self.stop_robot()
            return py_trees.common.Status.SUCCESS
    
    def update_tf_data(self):
        try:
            (trans_target, rot_target) = self.draw_square.tf_listener.lookupTransform('/base_link', self.target_frame, rospy.Time(0))
            self.point_x = trans_target[0]
            self.point_y = trans_target[1]
            self.point_angle_z = euler_from_quaternion(rot_target)[2]

            (trans_fork, rot_fork) = self.draw_square.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.fork_x = trans_fork[0]
            self.fork_y = trans_fork[1]
            self.fork_angle_z = euler_from_quaternion(rot_fork)[2]

            self.distance = sqrt((self.point_x - self.fork_x) ** 2 + (self.point_y - self.fork_y) ** 2)
            self.path_angle_err = atan2(self.point_y - self.fork_y, self.point_x - self.fork_x) - self.fork_angle_z
            
            return True

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logwarn(f"Failed to get TF data: {e}")
            return False

    def stop_robot(self):
        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        self.draw_square.move_cmd.publish(self.cmd_vel)
        rospy.loginfo("Stopping robot")

if __name__ == '__main__':
    try:
        draw_square = DrawSquare()
        draw_square.run()
    except rospy.ROSInterruptException:
        pass
