#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class Controller:

    def __init__(self):
        rospy.init_node("twist_to_gear_fork_drive_controls")
        
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        rospy.Subscriber('cmd_vel', Twist, self.cmd_callback, queue_size=10)
        self.linear_pub = rospy.Publisher('/gearfork_bot/cmd_vel', Twist, queue_size=10)
        self.steering_pub = rospy.Publisher('/gearfork_bot/steering_joint_controller/command', JointTrajectory, queue_size=10)
        rospy.loginfo("Steering Controller")

        self.joint_name = 'motor_joint'

        self.cmd_vel = Twist()
        self.steering_msg = JointTrajectory()
        self.point_msg = JointTrajectoryPoint()
        self.current_time = rospy.Duration(0)

        rospy.on_shutdown(self.shutdown_hook)
        self.timer = rospy.Timer(rospy.Duration(0.1), self.move_)

    def move_(self, event):
        self.steering_msg.header.stamp = rospy.Time.now()
        self.steering_msg.header.frame_id = ''
        self.steering_msg.joint_names = [self.joint_name]

        self.point_msg.positions = [self.angular_vel]
        self.steering_msg.points = [self.point_msg]
        self.point_msg.velocities = []
        self.point_msg.accelerations = []
        self.point_msg.effort = []

        self.cmd_vel.linear.x = self.linear_vel
        self.linear_pub.publish(self.cmd_vel)
        self.steering_pub.publish(self.steering_msg)

        rospy.loginfo(f"Linear Velocity --> {self.linear_vel}")
        rospy.loginfo(f"Angular Velocity --> {self.angular_vel}")

    def cmd_callback(self, msg):
        self.angular_vel = msg.angular.z
        self.linear_vel = msg.linear.x

    def shutdown_hook(self):
        rospy.logwarn("Node shutting down, stopping robot")
        self.angular_vel = 0.0
        self.linear_vel = 0.0
        self.move_(None)  # Publish zero velocities immediately

    def steering_controller(self):
        pass

def main():
    Controller()
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as e:
        rospy.logwarn(f"Shutting down: {e}")