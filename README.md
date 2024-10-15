# Bicycle-Kinematics-in-ROS


The kinematic bicycle model is a simplified model used in vehicle dynamics.

States:
x, y: Position coordinates of the vehicle in a global reference frame.
θ: Orientation angle of the vehicle relative to the global frame.
v: Forward velocity of the vehicle.

Inputs:
δ: Steering angle of the front wheels.
a: Longitudinal acceleration.


The position updates are based on the current position, orientation, velocity, steering angle, and time step.
The velocity updates are based on the current velocity and longitudinal acceleration.



#ROS Initialization and Publishers & visualization with RViz
The node initializes two ROS publishers
one for publishing the bicycle's position as a PoseStamped message  
another for visualizing the bicycle as a 3D marker in RViz using the Marker message.



The bicycle's position and orientation are sent as both PoseStamped and Marker messages to visualize the bicycle's motion.
bicycle is visualized as a blue cube in RViz.
Each time step logs the bicycle’s current time, position, 
