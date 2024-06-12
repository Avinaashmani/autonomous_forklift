#!/usr/bin/env python3

import serial
import rospy 
import actionlib

from std_msgs.msg import Bool
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class SendGoal:
    def __init__(self) -> None:
        
        rospy.init_node('button_goal', anonymous=False)
        rospy.loginfo_once("ESP32 Test 1")

        self.serial_port = '/dev/ttyUSB0'
        self.baud_rate = 9600

        try:
            self.esp32 = serial.Serial(self.serial_port, self.baud_rate, timeout=5)
            rospy.loginfo("Serial connection established.")
        except serial.serialutil.SerialException as e:
            rospy.logerr_once(f"Serial connection error: {e}")
            return
        
        self.trigger_goal()
        rospy.on_shutdown(self.shutdown_callback)

    def trigger_goal(self):
        while self.esp32.is_open and not rospy.is_shutdown():
            input_msg = self.esp32.readline().decode().strip()
            rospy.loginfo(f"Received message from ESP32: {input_msg}")

            if input_msg == "CALL":
                self.move_to_goal()
                rospy.loginfo(f"ESP Feedback: {input_msg}")

    def move_to_goal(self):
        rospy.loginfo("Preparing to send goal to move_base...")

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose.position.x = 1.90
        goal.target_pose.pose.position.y = -0.0025
        goal.target_pose.pose.position.z = 0.0

        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.707
        goal.target_pose.pose.orientation.w = 0.707

        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        client.wait_for_server()

        rospy.loginfo("Sending goal to move_base...")
        client.send_goal(goal)
        client.wait_for_result()
        rospy.loginfo("Goal execution finished.")

    def shutdown_callback(self):
        if self.esp32.is_open:
            self.esp32.close()
        rospy.logwarn_once("Exiting")

def main():
    SendGoal()
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except (rospy.ROSInternalException, rospy.ROSInterruptException) as e:
        rospy.logwarn_once(f"ROS error: {e}")
