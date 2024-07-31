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

        self.square_dimension = 3

    def publish_tf(self):
        rate = rospy.Rate(10)  # 10 Hz

        while not rospy.is_shutdown():
            tf1 = TransformStamped()
            tf1.header.stamp = rospy.Time.now()
            tf1.header.frame_id = self.base_frame
            tf1.child_frame_id = "point_1"

            # Set translation
            tf1.transform.translation.x = self.square_dimension
            tf1.transform.translation.y = 0.0
            tf1.transform.translation.z = 0.0

            # Set rotation (example rotation with only z and w components)
            tf1.transform.rotation.z = 0.0
            tf1.transform.rotation.w = 1.0

            tf2 = TransformStamped()
            tf2.header.stamp = rospy.Time.now()
            tf2.header.frame_id = "point_1"
            tf2.child_frame_id = "point_2"
            # Set translation
            tf2.transform.translation.x = 0.0
            tf2.transform.translation.y = self.square_dimension
            tf2.transform.translation.z = 0.0

            # Set rotation (example rotation with only z and w components)
            import math

            tf2.transform.rotation.z = -math.sqrt(2) / 2
            tf2.transform.rotation.w = math.sqrt(2) / 2

            tf3 = TransformStamped()
            tf3.header.stamp = rospy.Time.now()
            tf3.header.frame_id = "point_2"
            tf3.child_frame_id = "point_3"
            # Set translation
            tf3.transform.translation.x = 0.0
            tf3.transform.translation.y = -self.square_dimension
            tf3.transform.translation.z = 0.0

            # Set rotation (example rotation with only z and w components)
            tf3.transform.rotation.z = 0.0
            tf3.transform.rotation.w = 1.0

            tf4 = TransformStamped()
            tf4.header.stamp = rospy.Time.now()
            tf4.header.frame_id = self.base_frame
            tf4.child_frame_id = "starting_point"
            # Set translation
            tf4.transform.translation.x = 0.0
            tf4.transform.translation.y = 0.0
            tf4.transform.translation.z = 0.0

            # Set rotation (example rotation with only z and w components)
            tf4.transform.rotation.z = 0.0
            tf4.transform.rotation.w = 1.0

            self.tf_broadcaster.sendTransform(tf1)
            self.tf_broadcaster.sendTransform(tf2)
            self.tf_broadcaster.sendTransform(tf3)
            # self.tf_broadcaster.sendTransform(tf4)
            rate.sleep()

if __name__ == '__main__':
    try:
        pallet_tf = PalletTF()
        pallet_tf.publish_tf()
    except rospy.ROSInterruptException:
        rospy.logerr("ROS node terminated.")