#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

def send_command(position):
    pub = rospy.Publisher('/front_fork_position_controller/command', Float64, queue_size=10)
    rospy.init_node('send_command', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(position)
        pub.publish(position)
        rate.sleep()

if __name__ == '__main__':
    try:
        send_command(0.5)  # Send the desired position
    except rospy.ROSInterruptException:
        pass