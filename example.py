#!/usr/bin/env python

from tello_sim import Simulator

my_drone = Simulator()

# flight commands are below
my_drone.takeoff()
my_drone.move_forward(130)
my_drone.rotate_clockwise(90)
my_drone.move_forward(80)
my_drone.land()
