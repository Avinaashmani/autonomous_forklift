#!/usr/bin/env python3
import rospy
import requests
import tf2_ros
from geometry_msgs.msg import Transform, TransformStamped
from std_msgs.msg import String

class PalletDetection:
    
    def __init__(self):
        
        rospy.init_node('Pallet_Detector', anonymous=True)

        self.center = Transform()
        self.right = Transform()
        self.left = Transform()
        self.pallet_present = String()

        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        self.base_frame = 'odom'
        self.center_frame = 'pallet_center'
        self.left_pocket = 'left_pocket'
        self.right_pocket = 'right_pocket'
        
        self.center_pub = rospy.Publisher("/pallet_center", Transform, queue_size=10)
        self.right_pub = rospy.Publisher("/pallet_right", Transform, queue_size=10)
        self.left_pub = rospy.Publisher("/pallet_left", Transform, queue_size=10)
        self.pallet_presence_pub = rospy.Publisher('/pallet_presence', String, queue_size=10)
        
        rospy.Timer(rospy.Duration(0.1), self.read_camera)
    
    def read_camera(self, event):
        
        response = requests.get("http://192.168.1.10/api/detectionResult")
        
        self.left.translation.x = float((response.json()['data']['detectionResult']['leftPocket']['Z'])/ 1000)
        self.left.translation.y = float((response.json()['data']['detectionResult']['leftPocket']['X'])/ 1000)
        self.left.translation.z = float((response.json()['data']['detectionResult']['leftPocket']['Y'])/ 1000)
        
        self.right.translation.x = float((response.json()['data']['detectionResult']['rightPocket']['Z'])/ 1000)
        self.right.translation.y = float((response.json()['data']['detectionResult']['rightPocket']['X'])/ 1000)
        self.right.translation.z = float((response.json()['data']['detectionResult']['rightPocket']['Y'])/ 1000)
        
        self.center.translation.x = float((response.json()['data']['detectionResult']['centerPoint']['Z'])/ 1000)
        self.center.translation.y = float((response.json()['data']['detectionResult']['centerPoint']['X'])/ 1000)
        self.center.translation.z = float((response.json()['data']['detectionResult']['centerPoint']['Y'])/ 1000)
        
        self.center.rotation.z = float((response.json()['data']['detectionResult']['Angle'])/ 1000)

        pallet_present = response.json()['data']['detectionResult']['palletFound']

        rospy.loginfo(f"Left Pocket: {self.left.translation.x}-> Center Pocket {self.center.translation.x}<-{self.right.translation.x} Right Pocket : Pallet Presence ===> {pallet_present}")

        tf_center = TransformStamped()
        tf_center.header.stamp = rospy.Time.now()
        tf_center.header.frame_id = self.base_frame
        tf_center.child_frame_id = self.center_frame
        tf_center.transform.translation.x = self.center.translation.x
        tf_center.transform.translation.y = self.center.translation.y
        tf_center.transform.translation.z = 0.0

        tf_right = TransformStamped()
        tf_right.header.stamp = rospy.Time.now()
        tf_right.header.frame_id = self.base_frame
        tf_right.child_frame_id = self.right_pocket
        tf_right.transform.translation.x = self.right.translation.x
        tf_right.transform.translation.y = self.right.translation.y
        tf_right.transform.translation.z = 0.0   

        tf_left = TransformStamped()
        tf_left.header.stamp = rospy.Time.now()
        tf_left.header.frame_id = self.base_frame
        tf_left.child_frame_id = self.left_pocket
        tf_left.transform.translation.x = self.left.translation.x
        tf_left.transform.translation.y = self.left.translation.y
        tf_left.transform.translation.z = 0.0
        
        self.tf_broadcaster.sendTransform(tf_center)
        self.tf_broadcaster.sendTransform(tf_right)
        self.tf_broadcaster.sendTransform(tf_left)

        self.pallet_present.data = str(pallet_present)
        self.pallet_presence_pub.publish(self.pallet_present)

        self.center_pub.publish(self.center)
        self.right_pub.publish(self.right)
        self.left_pub.publish(self.left)

def main():
    PalletDetection()
    rospy.spin()
    
if __name__=='__main__':
    main()
