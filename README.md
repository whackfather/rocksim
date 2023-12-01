Rocket simulation code written in python. This is a constant work in progress.
Can also be used to simulate rocks if you so desire.

The motor simulation folder contains the code used to acquire the thrust curve and propellant mass of the rocket at any given time. It is designed to be used in modeling a custom motor, not a prebuilt one. There is not yet code to be used with a prebuilt motor.

flightprofile_v6.py is the main flight profile program. It runs based on the txt files gathered from motormathmodel_v3.py. Currently, flightprofile_v6.py is unfinished but ready for use.

We have future plans to add more degrees of freedom by including inclination and horizontal translation.
