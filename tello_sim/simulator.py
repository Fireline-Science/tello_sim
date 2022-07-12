import json
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
        self.takeoff_state = False
        self.altitude = 0
        self.cur_loc = (0,0)
        self.bearing = 0
        self.altitude_data = []
        self.path_coors = [(0,0)]
        self.flip_coors = []
        self.fig_count = 1
        self.command_log = []

    @staticmethod
    def serialize_command(command: dict):
        serialized = command['command']
        command_args = command.get('arguments', ())
        if len(command_args) > 0:
            serialized = '{} {}'.format(serialized, ' '.join([str(arg) for arg in command_args]))
        return serialized

    @staticmethod
    def check_flip_param(param: str):
        if param not in ["f", "b", "r", "l"]:
            raise Exception("I can't tell which way to flip. Please use f, b, r, or l")
        else:
            pass

    @staticmethod
    def check_int_param(param: int):
        if type(param) != int:
            raise Exception("One of the parameters of this command only accepts whole numbers without quotation marks.")
        else:
            pass

    def send_command(self, command: str, *args):
        # Command log allows for replaying commands to the actual drone
        command_json = {
            'command': command,
            'arguments': args
        }
        self.command_log.append(command_json)
        print('I am running your "{}" command.'.format(self.serialize_command(command_json)))

        time.sleep(2)

    # Control Commands
    def command(self):
        print("Hi! My name is TelloSim and I am your training drone.")
        print("I help you try out your flight plan before sending it to a real Tello.")
        print("I am now ready to take off. 🚁")
        self.send_command('command')

    def check_takeoff(self):
        if not self.takeoff_state:
            raise Exception("I can't do that unless I take off first!")
        else:
            print("I am flying at {} centimeters above my takeoff altitude.".format(self.altitude))
            pass

    # Plotting functions
    def plot_altitude_steps(self, e):
        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.plot(self.altitude_data,'ro', linestyle='dashed', linewidth=2, markersize=12)
        ax.plot(self.altitude_data, linewidth=e, alpha=.15)
        ax.grid()
        ax.set(xlabel='Step', ylabel='Altitude in Centimeters',title='Tello Altitude')
        plt.show()

    def plot_horz_steps(self, e):
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
        ax.set_xlim([xlowlim, xhilim])
        ax.set_ylim([ylowlim, yhilim])
        ax.plot(horz_df[0], horz_df[1], 'bo', linestyle='dashed', linewidth=2, markersize=12, label="Drone Moves")
        ax.plot(horz_df[0], horz_df[1], linewidth=e, alpha=.15)
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
        """
        Command drone to takeoff.

        Examples
        ----------
        drone.takeoff() # command drone to takeoff

        """
        if not self.takeoff_state:
            print("Get ready for takeoff!")
            self.takeoff_state = True
            self.altitude = self.takeoff_alt
            self.altitude_data.append(self.takeoff_alt)
            self.send_command('takeoff')
            print("My estimated takeoff altitude is {} centimeters".format(self.altitude))
        else:
            print("My current altitude is {} centimeters, so I can't takeoff again!".format(self.altitude))

    def land(self, e=25):
        """
        Command drone to land.

        Examples
        ----------
        drone.land() # command drone to land

        """
        self.check_takeoff()
        print("Get ready for landing!")
        self.takeoff_state = False
        self.altitude = 0
        self.send_command('land')
        print("Here are the graphs of your flight! I can't wait to try this for real.")
        self.plot_horz_steps(e)
        self.plot_altitude_steps(e)


    def up(self, dist: int, e=25):
        """
        Command drone to fly up a given number of centimeters.

        Parameters
        ----------
        dist : int
            the distance in centimeters
        e : int
            the width of the error bar in centimeters

        Examples
        ----------
        drone.up(100) # move drone up 100 centimeters

        """
        self.check_takeoff()
        self.check_int_param(dist)
        self.check_int_param(e)
        print("My current bearing is {} degrees.".format(self.bearing))
        self.altitude = self.altitude + dist
        self.altitude_data.append(self.altitude)
        self.send_command('up', dist)
        self.plot_altitude_steps(e)

    def down(self, dist: int, e=25):
        """
        Command drone to fly down a given number of centimeters.

        Parameters
        ----------
        dist : int
            the distance in centimeters
        e : int
            the width of the error bar in centimeters    

        Examples
        ----------
        drone.down(100) # move drone down 100 centimeters

        """
        self.check_takeoff()
        self.check_int_param(dist)
        self.check_int_param(e)
        print("My current bearing is {} degrees.".format(self.bearing))
        self.altitude = self.altitude - dist
        self.altitude_data.append(self.altitude)
        self.send_command('down', dist)
        self.plot_altitude_steps(e)

    def left(self, dist: int, e=25):
        """
        Command drone to fly left a given number of centimeters.

        Parameters
        ----------
        dist : int
            the distance in centimeters
        e : int
            the width of the error bar in centimeters

        Examples
        ----------
        drone.left(100) # move drone left 100 centimeters

        """
        self.check_takeoff()
        self.check_int_param(dist)
        self.check_int_param(e)
        print("My current bearing is {} degrees.".format(self.bearing))
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing-90, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        print(self.path_coors)
        self.send_command('left', dist)
        self.plot_horz_steps(e)

    def right(self, dist: int, e=25):
        """
        Command drone to fly right a given number of centimeters.

        Parameters
        ----------
        dist : int
            the distance in centimeters
        e : int
            the width of the error bar in centimeters

        Examples
        ----------
        drone.right(100) # move drone right 100 centimeters

        """
        self.check_takeoff()
        self.check_int_param(dist)
        self.check_int_param(e)
        print("My current bearing is {} degrees.".format(self.bearing))
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing+90, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('right', dist)
        self.plot_horz_steps(e)

    def forward(self, dist: int, e=25):
        """
        Command drone to fly forward a given number of centimeters.

        Parameters
        ----------
        dist : int
            the distance in centimeters
        e : int
            the width of the error bar in centimeters

        Examples
        ----------
        drone.forward(100) # move drone forward 100 centimeters

        """
        self.check_takeoff()
        self.check_int_param(dist)
        self.check_int_param(e)
        print("My current bearing is {} degrees.".format(self.bearing))
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('forward', dist)
        self.plot_horz_steps(e)

    def back(self, dist: int, e=25):
        """
        Command drone to fly backward a given number of centimeters.

        Parameters
        ----------
        dist : int
            the distance in centimeters
        e : int
            the width of the error bar in centimeters

        Examples
        ----------
        drone.back(100) # move drone backward 100 centimeters

        """
        self.check_takeoff()
        self.check_int_param(dist)
        self.check_int_param(e)
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing+180, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('back', dist)
        self.plot_horz_steps(e)

    def cw(self, degr: int):
        """
        Rotate drone clockwise.

        Parameters
        ----------
        degr : int

        Examples
        ----------
        drone.cw(90) # rotates drone 90 degrees clockwise

        """
        self.check_takeoff()
        self.check_int_param(degr)
        print("My current bearing is {} degrees.".format(self.bearing))
        self.bearing = self.bearing + (degr % 360)
        self.send_command('cw', degr)
        print("My new bearing is {} degrees.".format(self.bearing))

    def ccw(self, degr: int):
        """
        Rotate drone counter clockwise.

        Parameters
        ----------
        degr : int

        Examples
        ----------
        drone.ccw(90) # rotates drone 90 degrees counter clockwise

        """
        self.check_takeoff()
        self.check_int_param(degr)
        print("My current bearing is {} degrees.".format(self.bearing))
        self.bearing = self.bearing - (degr % 360)
        self.send_command('ccw', degr)
        print("My current bearing is {} degrees.".format(self.bearing))

    def flip(self, direc: str, e=25):
        """
        Flips drones in one of four directions:
        l - left
        r - right
        f - forward
        b - back

        Parameters
        ----------
        direc : str
            direction of flip
        e : int
            the width of the error bar in centimeters

        Examples
        ----------
        drone.flip("f") # flips drone forward

        """
        self.check_takeoff()
        self.check_flip_param(direc)
        self.check_int_param(e)
        self.send_command('flip', direc)
        self.flip_coors.append(self.cur_loc)
        self.plot_horz_steps(e)

    # Deploys the command log from the simulation state to the actual drone
    def deploy(self):
        """
        Deploys commands built up for drone object to real drone via easyTello.
        Note: computer must be connected to the drone's WiFi network.

        Examples
        ----------
        drone.deploy() # deploy commands to drone

        """
        print('Deploying your commands to a real Tello drone!')

        if (self.driver_instance is None):
            # Since the driver binds to a socket on instantiation, we can only
            # keep a single driver instance open per session
            self.driver_instance = Tello()

        for command in self.command_log:
            self.driver_instance.send_command(self.serialize_command(command))

    # Resets the simulation state back to the beginning: no commands + landed
    def reset(self):
        """
        Reset the drone object to initialization state.

        Examples
        ----------
        drone.reset() # reset sim state

        """
        print('Resetting simulator state...')
        self._init_state()
        self.command()

    def save(self, file_path='commands.json'):
        """
        Save commands from current sim state to a local file.

        Parameters
        ----------
        file_path : str

        Examples
        ----------
        drone.save("commands.json") # save current state to JSON file

        """
        print('Saving commands to {}'.format(file_path))
        with open(file_path, 'w') as json_file:
            json.dump(self.command_log, json_file, indent=4)

    def load_commands(self, file_path:str):
        """
        Load commands from a local file to the current sim object.
        See documentation for the required file format.

        Parameters
        ----------
        file_path : str

        Examples
        ----------
        drone.load_commands("commands.json") # load commands from file to current sim object.

        """
        self._init_state()
        print('Loading commands from {}'.format(file_path))
        with open(file_path) as json_file:
            commands = json.load(json_file)

        for command in commands:
            # TODO guard checks
            getattr(self, command['command'])(*command['arguments'])
