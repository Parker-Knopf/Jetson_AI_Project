# Object Password Prototype 
Jetson AI Specialist Project


In todays modern world, passwords are becoming more and more vunerable. A way this can be solved is to hide the password in a nuerual-net. One cannot uncover the password simply by looking at the nueuro-net, since it is too complicated. You must have the object the neuro-net is trained for. There are millions of objects in the world making each password entiely unique to the user. Using common objects as elements of a password would be very secure since you would first need to know what objects are valid elements and what order they go in.

This simple project is a prototype to display the use of a nuerual-net and objects to set passwords!

# Requirements

- Jetson Nano

- Micro SD card

- USB Camera
# Dependencies

Flow these required steps to set up the dependencies for this projects. If your Jetson Nano is already set up, you can skip steps 1 and 2.

1. Flash SD Card: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write

2. Set-up the Jetson Nano:

3. Set up the Jetson Hello AI Docker Container: 

- Download here: https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md

- Build from source: https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md

# Getting Started

4. Clone or download this Git Repository on the Jetson Nano and run setup.sh:
``` bash
$ cd ~/
$ git clone https://github.com/Parker-Knopf/Object_Password_Prototype.git
$ cd Object_Password_Prototype
$ chmod +x setup.sh
$ ./setup.sh
```

5. Run the docker container:
``` bash
$ cd ~/jetson-inference
$ docker/run.sh --volume ~/Object_Password_Prototype:/Object_Password_Prototype
$ cd /Object_Password_Prototype
```
# Runing the Program

6. To start the program navigate to the correct directory and start run.sh
``` bash
$ cd ~/Object_Password_Prototype
$ ./run.sh
```
- Point the camera frame to face a white background with good lighting
- Use the termial to navigate through the program by the given prompts
- Use a blue circle and square to as objects to follow the prompts given by the program
# Notes

- The inital run of this project will take a while depending on your machine. Give it some time to build the model.
- The model used is not trained for 2 specific objects: blue cicles and squares
- Squares that are tilted to be a dimond are not found by the nueral-net (seen as circles)
