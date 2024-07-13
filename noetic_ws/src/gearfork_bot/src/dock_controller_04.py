#!/usr/bin/env python3

import rospy
import rosparam
import tf
from math import sqrt, atan2, pi, cos, sin
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist, Point
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class DockPallet:

    def __init__(self):
        rospy.init_node('pallet_dock', anonymous=True)
        rosparam.load_file('/home/avinaash/autonomous_forklift/noetic_ws/src/gearfork_bot/config/pallet_docking_prams.yaml')

        self.pallet_x = 0.0
        self.pallet_y = 0.0
        self.pallet_angle = 0.0

        self.fork_x = 0.0
        self.fork_y = 0.0
        self.fork_angle = 0.0

        self.distance = 0.0
        self.path_angle_err = 0.0

        self.intermediate_distance = 0.0
        self.intermediate_path_angle = 0.0

        self.controlled_angle = 0.0

        self.move_cmd = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.steering_pub = rospy.Publisher('/gearfork_bot/steering_joint_controller/command', JointTrajectory, queue_size=10)
        self.tf_listener = tf.TransformListener()

        self.waypoints = []
        self.current_waypoint_index = 0
        self.waypoint_threshold = 0.2  # Threshold distance to consider waypoint reached

        self.cmd_vel = Twist()
        self.steering_msg = JointTrajectory()
        self.point_msg = JointTrajectoryPoint()

        self.control_timer = rospy.Timer(rospy.Duration(0.1), self.control_loop)
        rospy.on_shutdown(self.on_shutdown)

    def control_loop(self, event):
        self.update_tf_data()

        self.point_msg.velocities = []
        self.point_msg.accelerations = []
        self.point_msg.effort = []

        self.compute()

    def compute(self):
        if not self.waypoints:
            self.compute_waypoints()

        if self.current_waypoint_index < len(self.waypoints):
            self.navigate_to_waypoint(self.waypoints[self.current_waypoint_index])

    def compute_waypoints(self):
        # Calculate intermediate points along the arc to point H
        num_waypoints = 10  # Adjust number of waypoints as needed
        arc_radius = 1.0  # Adjust arc radius as needed

        dx = (self.pallet_x - self.fork_x)
        dy = (self.pallet_y - self.fork_y)
        distance_to_h = sqrt(dx ** 2 + dy ** 2)
        angle_to_h = atan2(dy, dx)

        self.waypoints = []
        for i in range(num_waypoints):
            theta = angle_to_h + (i / (num_waypoints - 1)) * pi / 2
            waypoint_x = self.fork_x + arc_radius * cos(theta)
            waypoint_y = self.fork_y + arc_radius * sin(theta)
            self.waypoints.append(Point(x=waypoint_x, y=waypoint_y))

    def navigate_to_waypoint(self, waypoint):
        # Calculate angle and distance to waypoint
        dx = waypoint.x - self.fork_x
        dy = waypoint.y - self.fork_y
        distance_to_waypoint = sqrt(dx ** 2 + dy ** 2)
        angle_to_waypoint = atan2(dy, dx) - self.fork_angle

        # Adjust angular velocity to align with the waypoint
        if abs(angle_to_waypoint) > 0.1:
            self.controlled_angle = angle_to_waypoint * 0.5
            self.cmd_vel.angular.z = self.controlled_angle
        else:
            self.controlled_angle = 0.0
            self.cmd_vel.angular.z = self.controlled_angle
        
        # Move towards the waypoint
        self.cmd_vel.linear.x = -(distance_to_waypoint / 10)
        
        # Publish velocities
        self.move_cmd.publish(self.cmd_vel)

        # Check if waypoint reached
        if distance_to_waypoint < self.waypoint_threshold:
            self.current_waypoint_index += 1

    def on_shutdown(self):
        rospy.logwarn("Node shutting down, stopping robot")
        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        self.move_cmd.publish(self.cmd_vel)

    def update_tf_data(self):
        try:
            (trans_pallet, rot_pallet) = self.tf_listener.lookupTransform('/odom', '/pallet_center', rospy.Time(0))
            self.pallet_x = trans_pallet[0]
            self.pallet_y = trans_pallet[1]
            self.pallet_angle = euler_from_quaternion(rot_pallet)[2]

            (trans_fork, rot_fork) = self.tf_listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
            self.fork_x = trans_fork[0]
            self.fork_y = trans_fork[1]
            self.fork_angle = euler_from_quaternion(rot_fork)[2]

            self.distance = sqrt((self.pallet_x - self.fork_x) ** 2 + (self.pallet_y - self.fork_y) ** 2)
            self.intermediate_distance = sqrt(((self.pallet_x + 3.0) - self.fork_x) ** 2 + (self.pallet_y - self.fork_y) ** 2)

            self.path_angle_err = atan2(self.pallet_y - self.fork_y, self.pallet_x - self.fork_x) - self.fork_angle
            self.intermediate_path_angle = atan2(self.pallet_y - self.fork_y, self.pallet_x - self.fork_x) - self.fork_angle

            rospy.loginfo(f"TF Data - Fork X: {self.fork_x}, Y: {self.fork_y}, Angle: {self.fork_angle}")
            rospy.loginfo(f"TF Data - Pallet X: {self.pallet_x}, Y: {self.pallet_y}, Angle: {self.pallet_angle}")
            rospy.loginfo(f"Distance to Pallet: {self.distance}, Path Angle Error: {self.path_angle_err}")

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("Failed to get TF data. Retrying...")

if __name__ == '__main__':
    try:
        DockPallet()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
