#!/usr/bin/env python3

import rospy 
import actionlib
from control_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from geometry_msgs.msg import Twist
from math import atan2

class CmdVelToJointTrajectory:

    def __init__(self):

        rospy.init_node('twist_to_joint_trajectory')
        self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.cmd_callback)

        self.action_client = actionlib.SimpleActionClient('/tricycle_test_bot_1/steering_joint_controller/follow_joint_trajectory/', FollowJointTrajectoryAction)
        rospy.loginfo("Waiting for joint trajectory action server...")
        self.action_client.wait_for_server()
        rospy.loginfo("Connected to joint trajectory action server")

        # Set the joint name
        self.joint_name = 'front_fork_joint'

        # Define the robot's parameters
        self.wheel_base = 0.5 

    def cmd_callback(self, msg):
        joint_traj = JointTrajectory()
        joint_traj.joint_names = [self.joint_name]

        # Calculate the steering angle from the angular velocity
        if msg.angular.z != 0:
            steering_angle = atan2(self.wheel_base * msg.angular.z, msg.linear.x)
        else:
            steering_angle = 0

        # Create a JointTrajectoryPoint
        point = JointTrajectoryPoint()
        point.positions = [steering_angle]
        point.velocities = [msg.angular.z]
        point.time_from_start = rospy.Duration(0.1)

        # Add the point to the joint trajectory
        joint_traj.points.append(point)

        # Create and send a FollowJointTrajectoryGoal
        goal = FollowJointTrajectoryGoal()
        goal.trajectory = joint_traj

        self.action_client.send_goal(goal)
        rospy.loginfo("Sent joint trajectory goal")

if __name__ == '__main__':
    try:
        CmdVelToJointTrajectory()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
