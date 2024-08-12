#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class Controller:

    def __init__(self):
        rospy.init_node("twist_to_forkamrtest3_drive_controls")
        
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        rospy.Subscriber('cmd_vel', Twist, self.cmd_callback, queue_size=10)
        self.linear_pub = rospy.Publisher('/forkamrtest3/velocity_joint_controller/command', Float64, queue_size=10)
        self.steering_pub = rospy.Publisher('/forkamrtest3/steering_joint_controller/command', JointTrajectory, queue_size=10)
        rospy.loginfo("Steering Controller")

        self.joint_name = 'motor_joint'

        self.cmd_vel = Float64()
        self.steering_msg = JointTrajectory()
        self.point_msg = JointTrajectoryPoint()

        self.steering_msg.joint_names = [self.joint_name]
        self.rate = rospy.Rate(10) 

    def cmd_callback(self, msg):
        self.angular_vel = msg.angular.z * 2
        self.cmd_vel.data = msg.linear.x * 10
        self.linear_vel = msg.linear.x

        self.steering_msg.header.stamp = rospy.Time.now()
        
        self.point_msg.positions = [self.angular_vel]
        self.point_msg.time_from_start = rospy.Duration(0.1)  

        self.steering_msg.points = [self.point_msg] 

        self.steering_pub.publish(self.steering_msg)     
        self.linear_pub.publish(self.cmd_vel)  

        rospy.loginfo(f" Linear Velocity --> {self.linear_vel}")
        rospy.loginfo(f" Angular Velocity --> {self.angular_vel}")

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

def main():
    controller = Controller()
    controller.run()
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as e:
        rospy.logwarn(f"Shutting down: {e}")
