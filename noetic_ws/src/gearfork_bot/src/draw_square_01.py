#!/usr/bin/env python3

import rospy
import rosparam
import tf
from math import sqrt, atan2, pi
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory

class DockPallet:

    def __init__(self):
        rospy.init_node('pallet_dock', anonymous=True)
        rosparam.load_file('/home/avinaash/autonomous_forklift/noetic_ws/src/gearfork_bot/config/pallet_docking_prams.yaml')

        self.fork_x = 0.0
        self.fork_y = 0.0
        self.fork_angle = 0.0
        
        self.distance = 0.0

        self.controlled_speed = 0.0

        self.move_cmd = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        self.tf_listener = tf.TransformListener()

        self.cmd_vel = Twist()

        self.kp_dist = 0.2
        self.kd_dist = 0.5
        self.rate = rospy.Rate(5)

        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.control_loop)  # type: ignore
        rospy.on_shutdown(self.on_shutdown)

    def control_loop(self, event):
        self.update_tf_data()
        self.draw_square(5)

    def draw_square(self, dimension):
        if dimension < 3:
            rospy.signal_shutdown("not large enough...")
        
        for i in range (0, 60):
            self.cmd_vel.linear.x = -0.5
            self.cmd_vel.angular.z = 0.0

            self.move_cmd.publish(self.cmd_vel)
            self.rate.sleep()
        
        rospy.loginfo("Turning Left")

        for i in range (0, 110):
            self.cmd_vel.linear.x = -0.12
            self.cmd_vel.angular.z = -1.0

            self.move_cmd.publish(self.cmd_vel)
            self.rate.sleep()

    def on_shutdown(self):
        rospy.loginfo("Shutting down DockPallet node")
        self.control_timer.shutdown()

        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        self.move_cmd.publish(self.cmd_vel)

        rospy.loginfo("DockPallet node shutdown complete")

    def update_tf_data(self):
        try:
            (trans_fork, rot_fork) = self.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.fork_x = round(trans_fork[0], 3)
            self.fork_y = round(trans_fork[1], 3)
            self.fork_angle = round(euler_from_quaternion(rot_fork)[2], 3)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("Failed to get TF data. Retrying...")

if __name__ == '__main__':
    try:
        DockPallet()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
