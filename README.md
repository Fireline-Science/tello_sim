# tello_sim

**tello_sim** is a simple Python simulator (sim) that can be used by students to test their [tello](https://www.ryzerobotics.com/tello-edu) flight plans before deploying them to a real drone. In this fork, it uses [DJITellopy](https://github.com/damiafuentes/DJITelloPy)

This is a fork of a previous project written by [Fireline-Science](https://github.com/Fireline-Science/tello_sim), so all credit goes to him for the heavy lifting. I simply am just updating it to help teach my classes.

One suggested use for the sim is to develop an in-class obstacle course for students to fly their drone through. For example, you could have designated launch and landing positions that are separated by a series of obstacles. Obstacles could include tunnels to fly through or corners to navigate around.

Depending on the skill level of the class, you can either break the class up into teams or have students work individually. Each team or student then needs to observe and measure the actual course to determine what command inputs will let them successfully fly through the course. The sim requires students to think through, develop, and test their entire flight plan via simple commands or scripts before deploying them to the real drone. When they run their simulation, it outputs some basic plots of the three dimensional paths the drone *should* take that can help them estimate how well their flight plan might work with the real drone.

We have included two supporting presentations in this repo in the "teaching_materials" folder. These provide an introduction to Python, simulations, and how to use this library. The "simulation_intro" presentation contains slides that can be used with students and the "simulation_teaching" presentation provides more background for educators.

After simulating their flight, they can then deploy the same code to a real drone to see how their model performs in the real world. In order to control the flight of the actual drones, the facilitator can take the output from each team or student (via the save command discussed below) and deploy it from a single computer. Students can then observe how different approaches work in the real world with the actual drone.

There will always be differences between the simulation and the actual flight which will help students think about how to evaluate their model and improve it given data from the real flight. For example, if the drone goes too high, they can adjust their command script to account for this observation.

An exercise like this supports the United States' Next Generation Science Standards for K12 related to [distinguishing between a model and the actual object, process, and/or events the model represents](https://ngss.nsta.org/Practices.aspx?id=2).  

The sim was developed for use in a Jupyter notebook or QT console so that the plots are displayed inline with the code print outputs. The sim currently supports a subset of the full DJI command set including: takeoff, land, forward, back, left, right, up, down, flip, cw, and ccw.

## Tello App for Android 12 (as of July 2022)
While the app is not required for using the simulator, you may need it to update the drone's firmware. As of July 2022, the app in the Google Play Store does not work with Android 12. You can download a version that does work directly at https://www.dji.com/downloads/djiapp/tello .

## Example Jupyter Notebook
![](/images/jupyter_notebook.png)



## Installation
To install the library from cloned source:
```
$ git clone https://github.com/Fireline-Science/tello_sim
$ cd tello_sim
$ pip install .
```

**Note:** The sim requires pandas and matplotlib and is designed to be used interactively with Jupyter notebooks or QT consoles. Downloading and installing the [Anaconda distribution](https://www.anaconda.com/distribution/) of Python 3 is the recommended method for getting these data science packages.

## Cloud Notebook Option
If you don't want to install Jupyter on your local machine, you can also use the free [mybinder](https://mybinder.org/) cloud-based Jupyter notebook service. While this service will allow you to use the simulator, you will not be able to deploy your simulated flight to a real drone given the code will be running on a remote server. We have used this in classrooms where we could not easily install Python. In this scenario, the students are able to work with the simulator in their browser and then share their final flight code with the teacher who has installed the library locally and can send it to the drone via WiFi.

Use the link below to launch the mybinder version of a Jupyter notebook and then you can open the demo notebook which is titled "drone_notebook.ipynb".

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Fireline-Science/tello_sim/master)




## Simulator Examples

The simulator is built to run interactively in a Jupyter notebook or QT Console. The sim class outputs both text prompts and plots with each
simulated command.

Creating a simulated drone object in Python:
```python
from tello_sim import Simulator

my_drone = Simulator()
```
![](/images/ready.png)

```python
my_drone.takeoff()
```
![](/images/takeoff.png)

```python
my_drone.move_forward(40)
```
![](/images/forward.png)

By default, the simulator plots a 25 cm error region in light blue around the flight path. For more advanced projects, you can override the default parameter by including the optional second error bar parameter in centimeters like ```forward(40, e=50)```. This is useful when you want to change the model (simulation) based on empirical (actual) testing.


```python
my_drone.rotate_counter_clockwise(45)
```
![](/images/cw.png)

```python
my_drone.move_forward(50)
```
![](/images/forward_2.png)

```python
my_drone.land()
```
![](/images/land.png)

## Saving and Loading Command scripts
In a classroom, it can be useful to allow students to share their command scripts or allow them to send them to a teacher which can be the gatekeeper for sending the scripts to the real drones. To facilitate that, we have two functions that allow you to save and load commands scripts. The scripts are a simple JSON document formatted as follows:

```json
[
    {
        "command": "command",
        "arguments": []
    },
    {
        "command": "takeoff",
        "arguments": []
    },
    {
        "command": "forward",
        "arguments": [
            100
        ]
    },
    {
    	"command": "rotate_counter_clockwise",
	"arguments": [
	    90
	]
    },
    {
    	"command": "move_forward",
	"arguments": [
	    100
	]
    },
    {
        "command": "land",
        "arguments": []
    }
]
```

To save the commands built up in an interactive console, do the following:

```python
my_drone.save(file_path='save_file.json')
```

To load a command file, do the following. Note that the `load_commands` function resets your drone object, so any saved commands will be cleared.

```python
my_drone.load_commands(file_path='new_commands.json')
```

## Resetting Simulator States
To reset the state of your simulator for a given object, use the following:

```python
my_drone.reset()
```

## Deploying to a Real Drone
We are using the [DJITellopy](https://github.com/damiafuentes/DJITelloPy) library to allow you to deploy your simulated flight to a real drone. Once you are connected to your drone via WiFi, you can deploy the commands you built up in an interactive session or loaded via a command file in Jupyter with the following command:

```python
my_drone.deploy()
```

We recommend that you spend some time experimenting with the simulator and deploying code to the drone prior to use in the classroom. The interface to the drone can experience errors when deploying commands which can generally be resolved by restarting the drone, reconnecting to the drone's WiFi network and using the library to rerun the `my_drone.deploy()` command. You can also set the expectation that errors do occur and are part of the general scientific process. We recommend that you refer to the [Tello User Manual](https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20User%20Manual%20v1.4.pdf) for general information about the drone. Of specific interest are the various LED codes which we have replicated below.

||Color|Pattern|Drone State|
|-------------|-----|-----|-----|
|**Normal States**|Alternating red, green, and yellow|Blinking|Turning on and performing self-diagnostic tests|
||Green|Periodically blinks twice|Vision positioning system active|
||Yellow|Blinking slowly|Vision unavailable (usually due to low light)||
|**Charging States**|Blue|Solid|Charging is complete|
||Blue|Blinking slowly|Charging|
||Blue|Blinking quickly|Charging error|
|**Warning States**|Yellow|Blnking quickly|Remote control signal lost|
||Red|Blnking slowly|Low battery|
||Red|Blnking quickly|Critically low battery|
||Red|Solid|Critical error|

## Running Multiple Command Scripts in the Same Session
Note: if you are running multiple scripts to the drone, you may have to kill the process that binds the python process to the Tello port if you receive a `OSError: [Errno 48] Address already in use` error. You can search for and kill the process as follows in a linux or MacOSX console. Replace XXXX with the process id that you see after running the `lsof` command.

```
lsof -i:8889
kill XXXX
```

If you're on Windows the following commands should work
```

netstat -p tcp -ano  | findstr ":21" (Outpuuted as Protocol Local Address Foreign Address State PID)
taskkill /F /ID XXXX
```