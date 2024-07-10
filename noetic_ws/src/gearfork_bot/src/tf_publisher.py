#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped

class PalletTF:
    def __init__(self):
        rospy.init_node('pallet_tf_publisher')
        rospy.loginfo_once('Pallet TF Publisher initialized')

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
            tf1.transform.translation.x = -2.0
            tf1.transform.translation.y = 0.2
            tf1.transform.translation.z = 0.0

            # Set rotation (example rotation with only z and w components)
            tf1.transform.rotation.z = 0.0
            tf1.transform.rotation.w = 1.0

            tf2 = TransformStamped()
            tf2.header.stamp = rospy.Time.now()
            tf2.header.frame_id = self.base_frame
            tf2.child_frame_id = self.left_pocket

            # Set translation
            tf2.transform.translation.x = -2.0
            tf2.transform.translation.y = -0.18
            tf2.transform.translation.z = 0.0

            # Set rotation (example rotation with only z and w components)
            tf2.transform.rotation.z = 0.0
            tf2.transform.rotation.w = 1.0

            tf3 = TransformStamped()
            tf3.header.stamp = rospy.Time.now()
            tf3.header.frame_id = self.base_frame
            tf3.child_frame_id = self.right_pocket
            # Set translation
            tf3.transform.translation.x = -2.0
            tf3.transform.translation.y = 0.0
            tf3.transform.translation.z = 0.0

            # Set rotation (example rotation with only z and w components)
            tf3.transform.rotation.z = 0.0
            tf3.transform.rotation.w = 1.0

            self.tf_broadcaster.sendTransform(tf1)
            self.tf_broadcaster.sendTransform(tf2)
            self.tf_broadcaster.sendTransform(tf3)
            rate.sleep()

if __name__ == '__main__':
    try:
        pallet_tf = PalletTF()
        pallet_tf.publish_tf()
    except rospy.ROSInterruptException:
        rospy.logerr("ROS node terminated.")
