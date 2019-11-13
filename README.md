# tello_sim

**tello_sim** is a simple Python simulator (sim) that can be used by students to test their DJI tello flight plans before deploying them to a real drone. It was inspired by the [easyTello](https://github.com/Virodroid/easyTello) library and uses it for the drone interface.

One suggested use for the sim is to develop an in-class obstacle course for students to fly their drone through. For example, you could have designated launch and landing positions that are separated by a series of obstacles. Obstacles could include tunnels to fly through or corners to navigate around. The sim requires students to think through, develop, and test their entire flight plan via the simple command scripts before deploying them to the drone. Using measurements from the real course, they can create command scripts to send to the simulator. The sim then outputs some basic plots of the three dimensional path the drone *should* take.

After simulating their flight, they can then deploy the same code to a real drone to see how their model performs in the real world. There will always be differences between the simulation and the actual flight which will help students think about how to evaluate their model and improve their flight plan given data from the real flight. An exercise like this supports the United States' Next Generation Science Standards for K12 related to [distinguishing between a model and the actual object, process, and/or events the model represents](https://ngss.nsta.org/Practices.aspx?id=2).  

The sim was developed for use in a Jupyter notebook or QT console so that the plots are displayed inline with the code print outputs. The sim currently supports a subset of the full DJI command set including: takeoff, land, forward, back, left, right, up, down, flip, cw, and ccw.

## Installation
<!-- To install the library, simply run:
```
pip install tello_sim
```
or to install from cloned source:
```
$ git clone https://github.com/Fireline-Science/tello_sim
$ cd tello_sim
$ pip install .
``` -->

**Note:** The sim requires pandas and is designed for use with Jupyter notebooks or QT consoles. Downloading and installing the [Anaconda distribution](https://www.anaconda.com/distribution/) of Python 3 is the recommended method for getting these data science packages.

## Sim Examples

The sim is built to run interactively in a Jupyter notebook or QT Console. The sim class outputs both text prompts and plots with each
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
my_drone.forward(40)
```
![](/images/forward.png)

```python
my_drone.cw(45)
```
![](/images/cw.png)

```python
my_drone.forward(50)
```
![](/images/forward_2.png)

```python
my_drone.land()
```
![](/images/land.png)

## Resetting Simulator States
To reset the state of your simulator for a given object, use the following:

```python
my_drone.reset()
```

## Deploying to a Real drone
We are using the [easytello](https://github.com/Virodroid/easyTello) library to allow you to deploy your simulated flight to a real drone. Once you are connected to your drone via WiFi, you can deploy the commands you built up in an interactive session in Jupyter with the following command:

```python
my_drone.deploy()
```



## Running Multiple Command Scripts in the Same Session
Note: if you are running multiple scripts to the drone, you may have to kill the process that binds the python process to the Tello port if you receive a `OSError: [Errno 48] Address already in use` error. You can search for and kill the process as follows in a linux-like console:

```
lsof -i:8889
kill XXXX
```
