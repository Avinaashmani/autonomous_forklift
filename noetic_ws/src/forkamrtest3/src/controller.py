#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class Controller:

    def __init__(self):
        rospy.init_node("twist_to_gear_fork_drive_controls")
        
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        rospy.Subscriber('/move_base/cmd_vel', Twist, self.cmd_callback, queue_size=10)
        self.linear_pub = rospy.Publisher('/forkamrtest3/cmd_vel', Twist, queue_size=10)
        rospy.loginfo("Steering Controller")

        self.joint_name = 'motor_joint'

        self.cmd_vel = Twist()
        self.steering_msg = JointTrajectory()
        self.point_msg = JointTrajectoryPoint()

        self.steering_msg.joint_names = [self.joint_name]
        self.rate = rospy.Rate(10) 

    def cmd_callback(self, msg):
        self.cmd_vel.linear.x = msg.linear.x
        self.cmd_vel.angular.z = msg.angular.z
    
        self.linear_pub.publish(self.cmd_vel)  

        rospy.loginfo(f" Linear Velocity --> {msg.linear.x}")
        rospy.loginfo(f" Angular Velocity --> {msg.angular.z}")

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
