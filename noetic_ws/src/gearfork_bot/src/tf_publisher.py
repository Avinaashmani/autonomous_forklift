#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped, Transform

class PalletTF:
    def __init__(self):
        rospy.init_node('pallet_tf_publisher')
        rospy.loginfo_once('Pallet TF Publisher initialized')

        rospy.Subscriber('/pallet_center', Transform, self.pallet_center, queue_size=10)
        rospy.Subscriber('/pallet_right', Transform, self.pallet_right, queue_size=10)
        rospy.Subscriber('/pallet_left', Transform, self.pallet_left, queue_size=10)

        self.center_x = 0.0
        self.center_y = 0.0
        self.center_z = 0.0
        self.center_rot_z = 1.0
        self.center_rot_w = 0.0

        self.right_x = 0.0
        self.right_y = 0.0
        self.right_z = 0.0
        self.right_rot_z = 1.0
        self.right_rot_w = 0.0

        self.left_x = 0.0
        self.left_y = 0.0
        self.left_z = 0.0
        self.left_rot_z = 1.0
        self.left_rot_w = 0.0

        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        self.base_frame = 'odom'
        self.child_frame = 'pallet_center'
        self.left_pocket = 'left_pocket'
        self.right_pocket = 'right_pocket'

    def publish_tf(self):
        rate = rospy.Rate(10)  # 10 Hz

        while not rospy.is_shutdown():
            tf1 = TransformStamped()
            tf1.header.stamp = rospy.Time.now()
            tf1.header.frame_id = self.base_frame
            tf1.child_frame_id = self.child_frame

            # Set translation
            tf1.transform.translation.x = self.center_x
            tf1.transform.translation.y = self.center_y
            tf1.transform.translation.z = self.center_z

            # Set rotation (example rotation with only z and w components)
            tf1.transform.rotation.z = self.center_rot_z
            tf1.transform.rotation.w = self.center_rot_w

            tf2 = TransformStamped()
            tf2.header.stamp = rospy.Time.now()
            tf2.header.frame_id = self.base_frame
            tf2.child_frame_id = self.right_pocket

            # Set translation
            tf2.transform.translation.x = self.right_x
            tf2.transform.translation.y = self.right_y
            tf2.transform.translation.z = self.right_z

            # Set rotation (example rotation with only z and w components)
            tf2.transform.rotation.z = self.right_rot_z
            tf2.transform.rotation.w = self.right_rot_w

            tf3 = TransformStamped()
            tf3.header.stamp = rospy.Time.now()
            tf3.header.frame_id = self.base_frame
            tf3.child_frame_id = self.left_pocket
            # Set translation
            tf3.transform.translation.x = self.left_x
            tf3.transform.translation.y = self.left_y
            tf3.transform.translation.z = self.left_z

            # Set rotation (example rotation with only z and w components)
            tf3.transform.rotation.z = self.left_rot_z
            tf3.transform.rotation.w = self.left_rot_w

            self.tf_broadcaster.sendTransform(tf1)
            self.tf_broadcaster.sendTransform(tf2)
            self.tf_broadcaster.sendTransform(tf3)
            rate.sleep()

    def pallet_center(self, msg):
        self.center_x = -msg.translation.x
        self.center_y = -msg.translation.y

    def pallet_right(self, msg):
        self.right_x = -msg.translation.x
        self.right_y = -msg.translation.y

    def pallet_left(self, msg):
        self.left_x = -msg.translation.x
        self.left_y = -msg.translation.y

if __name__ == '__main__':
    try:
        pallet_tf = PalletTF()
        pallet_tf.publish_tf()
    except rospy.ROSInterruptException:
        rospy.logerr("ROS node terminated.")
