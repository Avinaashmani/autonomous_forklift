#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Twist, TransformStamped, Vector3
from tf.transformations import quaternion_from_euler
from tf.broadcaster import TransformBroadcaster
import tf2_ros
import math

class TricycleKinematicController:
    def __init__(self):
        rospy.init_node('tricycle_kinematic_controller')

        # Parameters
        self.wheel_base = 2.5  # L
        self.x = 0.0  # X position
        self.y = 0.0  # Y position
        self.psi = 0.0  # Heading angle (ψ)

        self.current_time = rospy.Time.now()
        self.last_time = rospy.Time.now()

        # Publishers and Subscribers
        self.odom_pub = rospy.Publisher('/forkamrtest3/odom', Odometry, queue_size=10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)

        # Control inputs
        self.v = 0.0  # Linear velocity
        self.theta = 0.0  # Steering angle (θ)

        self.rate = rospy.Rate(10)  # 50 Hz update rate

    def cmd_vel_callback(self, msg):
        # Update control inputs from /cmd_vel
        self.v = msg.linear.x  # Forward velocity
        self.theta = msg.angular.z  # Steering angle (θ)

    def compute_odometry(self):
        self.current_time = rospy.Time.now()
        dt = (self.current_time - self.last_time).to_sec()

        if self.v != 0:  # Only update odometry if velocity is non-zero
            # Kinematic equations
            delta_x = self.v * math.cos(self.psi) * dt
            delta_y = self.v * math.sin(self.psi) * dt
            delta_psi = (self.v / self.wheel_base) * math.tan(self.theta) * dt

            # Update the position and heading angle
            self.x += delta_x
            self.y += delta_y
            self.psi += delta_psi

            # Normalize the angle to [-pi, pi]
            self.psi = (self.psi + math.pi) % (2 * math.pi) - math.pi

        self.last_time = self.current_time

    def publish_odometry(self):
        # Create an Odometry message
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "odom"  # Should be odom for fixed frame
        
        # Make vectors
        vector_ = Vector3()
        vector_.x = self.x 
        vector_.y = self.y
        vector_.z = 0.0

        # Set the position
        odom.pose.pose.position = vector_

        # Convert the heading angle to a quaternion
        quaternion = quaternion_from_euler(0, 0, self.psi)
        odom.pose.pose.orientation = Quaternion(*quaternion)

        # Set the velocity
        odom.child_frame_id = "base_link"  # The child frame should be base_link
        odom.twist.twist.linear.x = self.v
        odom.twist.twist.angular.z = (self.v / self.wheel_base) * math.tan(self.theta)

        # Publish the odometry message
        self.odom_pub.publish(odom)

        # Broadcast the transform from odom to base_link
        transform = TransformStamped()
        transform.header.stamp = rospy.Time.now()
        transform.header.frame_id = "odom"
        transform.child_frame_id = "base_link"
        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.translation.z = 0.0
        transform.transform.rotation.x = quaternion[0]
        transform.transform.rotation.y = quaternion[1]
        transform.transform.rotation.z = quaternion[2]
        transform.transform.rotation.w = quaternion[3]

        self.tf_broadcaster.sendTransform(transform)

    def run(self):
        while not rospy.is_shutdown():
            self.compute_odometry()
            self.publish_odometry()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        tricycle_controller = TricycleKinematicController()
        tricycle_controller.run()
    except rospy.ROSInterruptException:
        pass
