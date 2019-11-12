import time
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
import pandas as pd

from easytello import Tello


class Simulator():
    def __init__(self):
        self.takeoff_alt = 81
        self._init_state()
        self.driver_instance = None

        # Put drone into command mode
        self.command()

    def _init_state(self):
        self.altitude = 0
        self.cur_loc = (0,0)
        self.bearing = 0
        self.altitude_data = []
        self.path_coors = [(0,0)]
        self.flip_coors = []
        self.fig_count = 1
        self.command_log = []

    def send_command(self, command: str):
        print("I am running your {} command.".format(command))

        # Command log allows for replaying commands to the actual drone
        self.command_log.append(command)

        time.sleep(2)

    # Control Commands
    def command(self):
        print("Hi! My name is TelloSim and I am your training drone.")
        print("I help you try out your flight plan before sending it to a real Tello.")
        print("I am now ready to take off. 🚁")
        self.send_command('command')

    def check_altitude(self):
        if self.altitude == 0:
            raise Exception("I can't do that unless I take off first!")
        else:
            print("I am flying at {} centimeters above my takeoff altitude.".format(self.altitude))
            pass

    # Plotting functions
    def plot_altitude_steps(self):
        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.plot(self.altitude_data,'ro', linestyle='dashed', linewidth=2, markersize=12)
        ax.grid()
        ax.set(xlabel='Step', ylabel='Altitude in Centimeters',title='Tello Altitude')
        plt.show()

    def plot_horz_steps(self):
        title = "Path of Tello from Takeoff Location. \nLast Heading= {} Degrees from Start".format(self.bearing)
        fig, ax = plt.subplots()
        horz_df = pd.DataFrame(self.path_coors)
        xlow = min(horz_df[0])
        xhi = max(horz_df[0])
        ylow = min(horz_df[1])
        yhi = max(horz_df[1])
        xlowlim = -200 if xlow > -200 else xlow - 40
        xhilim = 200 if xhi < 200 else xhi + 40
        ylowlim = -200 if ylow > -200 else ylow - 40
        yhilim = 200 if yhi < 200 else yhi + 40
        ax.set_xlim([xlowlim,xhilim])
        ax.set_ylim([ylowlim,yhilim])
        ax.plot(horz_df[0], horz_df[1], 'bo', linestyle='dashed', linewidth=2, markersize=12, label="Drone Moves")
        if len(self.flip_coors) > 0:
            flip_df = pd.DataFrame(self.flip_coors)
            ax.plot(flip_df[0], flip_df[1], 'ro', markersize=12, label="Drone Flips")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid()
        ax.legend()
        ax.set(xlabel='X Distance from Takeoff', ylabel='Y Distance from Takeoff',title=title)
        plt.show()

    # Determine bearing relative to start which is inline with positive y-axis
    @staticmethod
    def dist_bearing(orig, bearing, dist):
        rads = np.deg2rad(bearing)
        sines = np.sin(rads)
        coses = np.cos(rads)
        dx = sines * dist
        dy = coses * dist
        x_n = np.cumsum(dx) + orig[0]
        y_n = np.cumsum(dy) + orig[1]
        return x_n[0], y_n[0]

   # Movement Commands
    def takeoff(self):
        if self.altitude == 0:
            print("Get ready for takeoff!")
            self.altitude = self.takeoff_alt
            self.altitude_data.append(self.takeoff_alt)
            self.send_command('takeoff')
            print("My estimated takeoff altitude is {} centimeters".format(self.altitude))
        else:
            print("My current altitude is {} centimeters, so I can't takeoff again!".format(self.altitude))

    def land(self):
        print("Get ready for landing!")
        self.check_altitude()
        self.altitude = 0
        self.send_command('land')
        print("Here are the graphs of your flight! I can't wait to try this for real.")
        self.plot_horz_steps()
        self.plot_altitude_steps()

    def up(self, dist: int):
        self.check_altitude()
        print("My current bearing is {} degrees.".format(self.bearing))
        self.altitude = self.altitude + dist
        self.altitude_data.append(self.altitude)
        self.send_command('up {}'.format(dist))
        self.plot_altitude_steps()

    def down(self, dist: int):
        self.check_altitude()
        print("My current bearing is {} degrees.".format(self.bearing))
        self.altitude = self.altitude - dist
        self.altitude_data.append(self.altitude)
        self.send_command('down {}'.format(dist))
        self.plot_altitude_steps()

    def left(self, dist: int):
        self.check_altitude()
        print("My current bearing is {} degrees.".format(self.bearing))
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing-90, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        print(self.path_coors)
        self.send_command('left {}'.format(dist))
        self.plot_horz_steps()

    def right(self, dist: int):
        self.check_altitude()
        print("My current bearing is {} degrees.".format(self.bearing))
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing+90, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('right {}'.format(dist))
        self.plot_horz_steps()

    def forward(self, dist: int):
        self.check_altitude()
        print("My current bearing is {} degrees.".format(self.bearing))
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('forward {}'.format(dist))
        self.plot_horz_steps()

    def back(self, dist: int):
        self.check_altitude()
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing+180, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('back {}'.format(dist))
        self.plot_horz_steps()

    def cw(self, degr: int):
        self.check_altitude()
        print("My current bearing is {} degrees.".format(self.bearing))
        self.bearing = self.bearing + (degr % 360)
        self.send_command('cw {}'.format(degr))
        print("My new bearing is {} degrees.".format(self.bearing))

    def ccw(self, degr: int):
        self.check_altitude()
        print("My current bearing is {} degrees.".format(self.bearing))
        self.bearing = self.bearing - (degr % 360)
        self.send_command('ccw {}'.format(degr))
        print("My current bearing is {} degrees.".format(self.bearing))

    def flip(self, direc: str):
        self.check_altitude()
        self.send_command('flip {}'.format(direc))
        self.flip_coors.append(self.cur_loc)
        self.plot_horz_steps()

    # Deploys the command log from the simulation state to the actual drone
    def deploy(self):
        print('Deploying your commands to a real Tello drone!')

        if (self.driver_instance is None):
            # Since the driver binds to a socket on instantiation, we can only
            # keep a single driver instance open per session
            self.driver_instance = Tello()

        for command in self.command_log:
            self.driver_instance.send_command(command)

    # Resets the simulation state back to the beginning: no commands + landed
    def reset(self):
        print('Resetting simulator state...')
        self._init_state()
        self.command()

    def save(self):
        print('Saving commands to commands.csv')
        commands = pd.DataFrame(self.command_log)
        commands.to_csv('commands.csv', index=False, header=False)

    # def load_commands(self, file_name:str):
    #     print('Loading commands from {}'.format(file_name))
    #     commands = pd.read_csv(file_name, header=None)
    #     com_list = commands[0].to_list()
    #     self.command_log = com_list
    #     for i in command_log:
    #
