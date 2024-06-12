#!/usr/bin/env python3

import socket
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class SendGoal:
    def __init__(self) -> None:
        rospy.init_node('button_goal', anonymous=False)
        rospy.loginfo("ESP32 Test 1")

        rospy.on_shutdown(self.shutdown_callback)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.goal_in_progress = False

        self.start_server()

    def start_server(self, host='0.0.0.0', port=12345):
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        rospy.loginfo(f"Server listening on {host}:{port}")

        self.move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        self.move_base_client.wait_for_server()

        while not rospy.is_shutdown():
            client_socket, client_address = self.server_socket.accept()
            rospy.loginfo(f"Connection from {client_address}")

            data = client_socket.recv(1024).decode().strip()
            rospy.loginfo(f"Received data: {data}")

            if self.goal_in_progress:
                rospy.logwarn("A goal is already in progress. Ignoring new goal request.")
                client_socket.sendall("Executing a goal".encode())
            else:
                if data == 'CALL':
                    self.goal_in_progress = True
                    self.move_to_goal()
                    self.goal_in_progress = False
                elif data == 'HOME':
                    self.goal_in_progress = True
                    self.home_goal()
                    self.goal_in_progress = False
            client_socket.close()

    def move_to_goal(self):
        rospy.loginfo("Work Position")

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

        rospy.loginfo("Sending goal to move_base...")
        self.move_base_client.send_goal(goal)
        self.move_base_client.wait_for_result()
        rospy.loginfo("Goal execution finished.")

    def home_goal(self):
        rospy.loginfo("Home Position")

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose.position.x = -2.3
        goal.target_pose.pose.position.y = 0.023
        goal.target_pose.pose.position.z = 0.0

        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.028
        goal.target_pose.pose.orientation.w = 1.0

        rospy.loginfo("Sending goal to move_base...")
        self.move_base_client.send_goal(goal)
        self.move_base_client.wait_for_result()
        rospy.loginfo("Goal execution finished.")

    def shutdown_callback(self):
        rospy.logwarn("Shutting down server")
        self.server_socket.close()

def main():
    SendGoal()
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except (rospy.ROSInternalException, rospy.ROSInterruptException) as e:
        rospy.logwarn(f"ROS error: {e}")
