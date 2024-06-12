#!/usr/bin/env python3

import rospy
import tf2_ros
from geometry_msgs.msg import Vector3, TransformStamped
from std_msgs.msg import Bool, String
import tf
import requests

class PalletDetection():
    
    def __init__(self):

        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        
        self.center = Vector3()
        self.right = Vector3()
        self.left = Vector3()

        self.pallet_presence = Bool()

        self.Q_size = 10
        
        self.center_pub = rospy.Publisher('pallet/center', Vector3, queue_size=self.Q_size)
        self.right_pub = rospy.Publisher('pallet/right', Vector3, queue_size=self.Q_size)
        self.left_pub = rospy.Publisher('pallet/left', Vector3, queue_size=self.Q_size)
        self.pallet_pub = rospy.Publisher('pallet/presence', Bool, queue_size=self.Q_size)

        self.base_frame = 'map'
        self.center_frame_id = 'pallet_center'
        self.left_frame_id = 'pallet_left'
        self.right_frame_id = 'pallet_right'
    
    def read_camera(self):
        
        while True:
            
            response =requests.get("http://192.168.1.10/api/detectionResult")
            
            self.left.x = float(response.json()['data']['detectionResult']['leftPocket']['Z'])
            self.left.y = float(response.json()['data']['detectionResult']['leftPocket']['X'])
            self.left.z = float(response.json()['data']['detectionResult']['leftPocket']['Y'])
            
            self.right.x = float(response.json()['data']['detectionResult']['rightPocket']['Z'])
            self.right.y = float(response.json()['data']['detectionResult']['rightPocket']['X'])
            self.right.z = float(response.json()['data']['detectionResult']['rightPocket']['Y'])
            
            self.center.x = float(response.json()['data']['detectionResult']['centerPoint']['Z'])
            self.center.y = float(response.json()['data']['detectionResult']['centerPoint']['X'])
            self.center.z = float(response.json()['data']['detectionResult']['centerPoint']['Y'])
            
            self.left.x = self.left.x  / 1000
            self.left.y = self.left.y  / 1000
            self.left.z = self.left.z  / 1000
            
            self.right.x = self.right.x  / 1000
            self.right.y = self.right.y  / 1000
            self.right.z = self.right.z  / 1000

            self.center.x = self.center.x  / 1000
            self.center.y = self.center.y  / 1000
            self.center.z = self.center.z  / 1000

            pallet_presence = response.json()['data']['detectionResult']['palletFound']

            pallet_center = TransformStamped()
            pallet_center.header.stamp = rospy.Time.now()
            pallet_center.child_frame_id = self.center_frame_id
            pallet_center.header.frame_id = self.base_frame
            pallet_center.transform.translation.x = self.center.x
            pallet_center.transform.translation.y = self.center.y
            # pallet_center.transform.translation.z = self.center.z
            pallet_center.transform.rotation.z = 1.0
            pallet_center.transform.rotation.w = 0.0

            pallet_right = TransformStamped()
            pallet_right.header.stamp = rospy.Time.now()
            pallet_right.child_frame_id = self.right_frame_id
            pallet_right.header.frame_id = self.base_frame
            pallet_right.transform.translation.x = self.right.x
            pallet_right.transform.translation.y = self.right.y
            # pallet_right.transform.translation.z = self.right.z
            pallet_right.transform.rotation.z = 1.0
            pallet_right.transform.rotation.w = 0.0

            pallet_left = TransformStamped()
            pallet_left.header.stamp = rospy.Time.now()
            pallet_left.header.frame_id = self.base_frame
            pallet_left.transform.translation.x = self.left.x
            pallet_left.transform.translation.y = self.left.y
            # pallet_left.transform.translation.z = self.left.z
            pallet_left.transform.rotation.z = 1.0
            pallet_left.transform.rotation.w = 0.0
            print(f"Left Pocket: {self.left.x}-> Center Pocket {self.center.x}<-{self.right.x} Right Pocket")

            if pallet_presence == 'true':
                self.pallet_presence.data = True
                self.center_pub.publish(self.center)
                self.left_pub.publish(self.left)
                self.right_pub.publish(self.right)
                self.pallet_pub.publish(self.pallet_presence)

                self.tf_broadcaster.sendTransform(pallet_center)
                self.tf_broadcaster.sendTransform(pallet_left)
                self.tf_broadcaster.sendTransform(pallet_right)

            else:
                self.pallet_presence.data = False
                self.pallet_pub.publish(self.pallet_presence)

def main():

    pallet_publisher = PalletDetection()
    while not rospy.is_shutdown:
        pallet_publisher
        rospy.spin()
        rospy.Rate(10).sleep()

if __name__=='__main__':
    try:
        main()

    except rospy.ROSInterruptException:
        pass
