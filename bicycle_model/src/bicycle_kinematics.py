#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker
import math

# Bicycle param
L = 1.0  # length (meters)
delta = 0.1  # Steering angle (radians)
v = 1.0  # velocity (mps)
phi = 0.05  # steering rate (rps)

# Initialize the state variables
x = 0.0
y = 0.0
theta = 0.0  # Heading angle

def compute_position(dt):
    global x, y, theta, delta, v

    # Update kinematic model equations
    x_dot = v * math.cos(theta + delta)
    y_dot = v * math.sin(theta + delta)
    theta_dot = (v * math.sin(delta)) / L
    delta_dot = phi

    # Update state over time step dt
    x += x_dot * dt
    y += y_dot * dt
    theta += theta_dot * dt
    delta += delta_dot * dt

    return x, y, theta

def bicycle_kinematics():
    rospy.init_node('bicycle_kinematics', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    #publishers for PoseStamped and Marker messages
    pose_pub = rospy.Publisher('/bicycle_pose', PoseStamped, queue_size=10)
    marker_pub = rospy.Publisher('/bicycle_marker', Marker, queue_size=10)

    t = 0.0
    dt = 0.1  # Time step

    while not rospy.is_shutdown():
        # Compute the new position and heading angle
        x, y, theta = compute_position(dt)

        # Create and publish the PoseStamped message
        pose_msg = PoseStamped()
        pose_msg.header.stamp = rospy.Time.now()
        pose_msg.header.frame_id = "map"

        # Set the position
        pose_msg.pose.position.x = x
        pose_msg.pose.position.y = y
        pose_msg.pose.position.z = 0.0  # Assume flat ground

        # Set the orientation (quaternion from theta)
        pose_msg.pose.orientation.z = math.sin(theta / 2.0)
        pose_msg.pose.orientation.w = math.cos(theta / 2.0)

        pose_pub.publish(pose_msg)

        # Create and publish the Marker message
        marker_msg = Marker()
        marker_msg.header.stamp = rospy.Time.now()
        marker_msg.header.frame_id = "map"
        
        # Set the marker's type (CUBE, SPHERE, etc.)
        marker_msg.type = Marker.CUBE

        # Set the marker's pose (same as the bicycle's pose)
        marker_msg.pose.position.x = x
        marker_msg.pose.position.y = y
        marker_msg.pose.position.z = 0.0
        marker_msg.pose.orientation.z = math.sin(theta / 2.0)
        marker_msg.pose.orientation.w = math.cos(theta / 2.0)

        # Set the marker's scale (size of the bicycle)
        marker_msg.scale.x = 1.0  # Length of the bicycle
        marker_msg.scale.y = 0.5  # Width of the bicycle
        marker_msg.scale.z = 0.2  # Height of the bicycle

        # Set the marker's color (RGBA)
        marker_msg.color.r = 0.0
        marker_msg.color.g = 0.0
        marker_msg.color.b = 1.0  # Blue bicycle
        marker_msg.color.a = 1.0  # Fully opaque

        marker_pub.publish(marker_msg)

        # Log the output for debugging
        rospy.loginfo(f"Time: {t:.2f}, Position -> x: {x:.2f}, y: {y:.2f}, θ: {theta:.2f}")

        # Update time
        t += dt

        rate.sleep()

if __name__ == '__main__':
    try:
        bicycle_kinematics()
    except rospy.ROSInterruptException:
        pass
