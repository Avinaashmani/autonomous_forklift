#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from std_msgs.msg import Float64
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import JointTrajectoryControllerState
import tf
import math

class TricycleOdometry:
    def __init__(self):
        rospy.init_node('tricycle_odometry')

        # Parameters
        # self.wheel_base = rospy.get_param('~wheel_base', 1.0)  # Distance between front and rear wheels
        self.rate = rospy.Rate(10)  # 10 Hz

        # Subscribers
        # rospy.Subscriber('/gearfork_bot/velocity_joint_controller/command', Float64, self.velocity_callback)
        rospy.Subscriber('/gearfork_bot/steering_joint_controller/command', JointTrajectory, self.steering_angle_callback)

        rospy.Subscriber('/cmd_vel', Twist, self.twist_callback)

        # Publishers
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
        self.odom_broadcaster = tf.TransformBroadcaster()

        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0

        self.x_new = 0.0
        self.y_new = 0.0
        self.th_new = 0.0
        
        self.current_velocity = 0.0
        self.steering_angle = 0.0

        self.wheelbase = 1.0
        self.radius_of_wheel = 0.1
        self.delta_t = 0.1

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.current_time = rospy.Time.now()
        self.last_time = rospy.Time.now()

    def velocity_callback(self, msg):
        if msg.data != 0:
            self.current_velocity = msg.data
        else:
            self.current_velocity = 0.0

    def steering_angle_callback(self, msg):
        if msg.points[0].positions[0] != 0:
            self.steering_angle = msg.points[0].positions[0]
        else:
            self.steering_angle = 0.0

    def twist_callback(self, msg):
        if not abs(msg.linear.x) == 0.0:
            self.current_velocity = msg.linear.x
        
        else:
            self.x = 0.0
            self.y = 0.0 
            self.theta = 0.0

    def compute_odometry(self):
        # icc = self.wheelbase/ math.tan(self.steering_angle)
        omega = self.current_velocity * math.tan(self.steering_angle)/self.wheelbase
        
        self.th_new = self.th + omega * self.delta_t

        self.delta_x = self.current_velocity * math.cos(self.th + self.steering_angle) * self.delta_t
        self.delta_y = self.current_velocity * math.sin(self.th + self.steering_angle) * self.delta_t

        self.x_new = self.x + self.delta_x
        self.y_new = self.y + self.delta_y

        self.x = self.x_new
        self.y = self.y_new
        self.th = self.th_new
        print(self.current_velocity)
        print(self.steering_angle)
        print(f"Robot Positions: x{self.x}, y={self.y}, theta={self.th}")

    def publish_odometry(self):
        pass

    def spin(self):
        while not rospy.is_shutdown():
            self.compute_odometry()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        tricycle_odometry = TricycleOdometry()
        tricycle_odometry.spin()
    except rospy.ROSInterruptException:
        pass
