#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from trajectory_msgs.msg import JointTrajectory
from tf.transformations import quaternion_from_euler
import tf
import math

class TricycleOdometry:
    def __init__(self):
        rospy.init_node('tricycle_odometry')

        # Parameters
        self.wheelbase = rospy.get_param('~wheelbase', 1.0)  # Distance between front and rear wheels
        self.rate = rospy.Rate(10)  # 10 Hz

        # Subscribers
        rospy.Subscriber('/gearfork_bot/velocity_joint_controller/command', Float64, self.velocity_callback)
        rospy.Subscriber('/gearfork_bot/steering_joint_controller/command', JointTrajectory, self.steering_angle_callback)
        # rospy.Subscriber('/cmd_vel', Twist, self.twist_callback)

        # Publishers
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
        self.odom_broadcaster = tf.TransformBroadcaster()

        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0

        self.current_velocity = 0.0
        self.steering_angle = 0.0

        self.last_time = rospy.Time.now()

    def velocity_callback(self, msg):
        self.current_velocity = msg.data

    def steering_angle_callback(self, msg):
        self.steering_angle = msg.points[0].positions[0]

    def twist_callback(self, msg):
        self.current_velocity = msg.linear.x

    def compute_odometry(self):
        current_time = rospy.Time.now()
        dt = (current_time - self.last_time).to_sec()

        if self.current_velocity != 0.0:
            # Calculate angular velocity
            omega = self.current_velocity * math.tan(self.steering_angle) / self.wheelbase

            # Update orientation
            self.th += omega * dt

            # Update position
            self.x += self.current_velocity * math.cos(self.th) * dt
            self.y += self.current_velocity * math.sin(self.th) * dt

        self.last_time = current_time

    def publish_odometry(self):
        current_time = rospy.Time.now()

        # Create odometry message
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        # Set position
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = quaternion_from_euler(0, 0, self.th)

        # Set velocity
        odom.twist.twist.linear.x = self.current_velocity
        odom.twist.twist.angular.z = self.current_velocity * math.tan(self.steering_angle) / self.wheelbase

        # Publish odometry
        self.odom_pub.publish(odom)

        # Broadcast transform
        self.odom_broadcaster.sendTransform(
            (self.x, self.y, 0),
            quaternion_from_euler(0, 0, self.th),
            current_time,
            "base_link",
            "odom"
        )

    def spin(self):
        while not rospy.is_shutdown():
            self.compute_odometry()
            self.publish_odometry()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        tricycle_odometry = TricycleOdometry()
        tricycle_odometry.spin()
    except rospy.ROSInterruptException:
        pass
