# Design Make and Test Group 16 (Electronics)
> Members of Electronics Group: Pike Amornchat, Nicholas Kwok, Jimmy van de Worp

> Supervisors: Dr Mike Bluck, Dr Matthew Eaton, Dr Antonis Sergis, Prof Yannis Hardalupas
## Project Brief

The mixing of hot and cold fluids in a T-junction is a scenario that is present in nuclear power plants, particularly between the intersection of the Reactor Pressure Vessel (RPV), Steam Generator (SG) and Pressuriser (PRZ) in a Pressurised Water Reactor (PWR). 

A well-known issue with T-junctions in PWRs is thermal fatigue phenomena. Previous failures include pipe ruptures in Japan and France mainly due to temperature fluctuations in the T-junctions causing high cycle thermal fatigue. 

In this super project, the intention is to design, make and test an experimental nuclear thermal-hydraulic rig (able to fit on a table) to both quantitatively and qualitatively characterise fluid flow in a transparent section and transient heat transfer effects in a stainless-steel opaque section. 

Experimental data from thermocouples will be captured through a data acquisition software and compared to Computational Fluid Dynamics (CFD) models. 

The wider test bed rig, which consists of all necessary auxiliary subassemblies to precisely control temperature and flow rate, will be closely integrated with the transparent and opaque section in a way such that the experimentalist can easily switch in and out sections. 

The super project is the start of a wider initiative to understand the transient thermo-fluid induced stresses in a T-junction more comprehensively, and a key objective of this project is to provide extensibility of the platform so that future research into continuous health monitoring (CHM) and non-destructive evaluation (NDE) methods can be conducted.

In summary, the rig's primary goal is:
* Understand the fluid mechanics and thermal fatigue phenomena in a T-junction and provide future extensibility for research into CHM and NDE methods.
* Validation of CFD results from test data obtained.
* A novel platform to train both undergraduates and postgraduates on thermal hydraulic diagnostics.

### The aim of this subgroup - DMT16 DAQ

More specifically, this section of the group was created to deal with the wide range of electronic demands of the project. 

The main tasks were:
* To produce an intuitive GUI which allowed the user to control the initial conditions and boundary conditions
* To install and synchronise all of the measurements such that a time reference can be assigned to each measurement
* To control the actuators in order to produce the desired transient boundary conditions

## Prerequisites

Must haves:

* VS Code (highly recommended) or suitable IDE (like PyCharm).  Note that Anaconda environments will not work
* Clone this repository on your PC
* Please see `Modules.py` in `server/`
* Flask for Python, if using the JavaScript UI, i.e., use ` $ pip install Flask `
* Google Chrome to run the JavaScript UI 
* Moesif CORS Extension for Google Chrome

* MacOS or Windows

Optional (if you would like to edit and re-flash STM32 or Arduino code):

* STM32 Cube MX
* STM32 Programmer
* STM32 IDE
* Arduino IDE 


### Installing the JavaScript UI 

The first step to install the JavasScript UI is to install the package manager, yarn. 

If on Windows, use Command Prompt, and on Mac use the terminal in VS Code:

```
npm install --global yarn
```

Now install the JavaScript UI (this should take a while to install):

```
cd client
yarn install --production
```

If you encounter errors for Windows, enter the commands into Command Prompt: 

```
set NODE_OPTIONS=--openssl-legacy-provider
```

If you encounter errors for Mac, enter the commands into the VS Code terminal:

```
export NODE_OPTIONS=--openssl-legacy-provider
```

Now your JavaScript UI should be installed, and you should have a new folder within `client/` called `node_modules`. 

## Setting up the Raspberry Pi from scratch
> THIS STEP IS ONLY NECESSARY IF THE RASPBERRY PI HAS BEEN THROUGH A FACTORY RESET 

To Setup from Unboxing:
* Install the Raspberry Pi Imager on Desktop.
* Write the 32-Bit Raspberry Pi OS on the SD Card using the Imager.
* Create Account
    * Username: icl-dmt16
    * Password: password

### To install PicoTech Drivers:

Connect to WiFi, open terminal, and update Raspberry Pi Source Packages List: 

```
$ sudo apt update && sudo apt upgrade
```

Import Public Key
```
$ wget -qO - https://labs.picotech.com/Release.gpg.key | sudo apt-key add
```

Configure your system repository

```
$ sudo bash -c 'echo "deb https://labs.picotech.com/picoscope7/debian/ picoscope main" >/etc/apt/sources.list.d/picoscope7.list'
```

Update package manager cache:

```
$ sudo apt-get update
```

Download the .deb file on the Raspberry Pi

```
$ wget https://labs.picotech.com/debian/pool/main/libu/libusbtc08/libusbtc08_2.0.17-1r1441_armhf.deb 
```

Install the .deb file on the Raspberry Pi

```
$ sudo apt install ./libusbtc08_2.0.17-1r1441_armhf.deb
```

### Installing Git and Obtaining Source Code

Create a working folder called icl-dmt16 and CD into that folder:

```
$ mkdir icl-dmt16
$ cd icl-dmt16
```

Installing Git: 

```
$ sudo apt-get install git
```

Adding Username Attributes To Local Git Account:

```
$ git config –global user.name “nk965”
```

Adding Email Attributes To Local Git Account:

```
$ git config –global user.email “nyk20@ic.ac.uk”
```

Clone Repository:

```
$ git clone https://github.com/nk965/DMT16_DAQ.git 
```

### Authorising Serial Ports: 

Open Raspberry Pi configuration: 

```
$ sudo raspi-config
```

* Follow Path:
    * 3 Interfacing Options
    * I6 Serial Port
    * Login shell Over Serial Port? NO
    * Serial Hardware Port Enabled? YES
    * OK
    * Finish
*	Reboot

``` 
$ sudo reboot
```

### Installing packages

Install pandas:

```
$ pip install pandas
```

Install seaborn:

```
$ sudo apt-get install libatlas-base-dev
```

Update numpy:

```
$ pip install seaborn
```

Install pigio:

```
$ sudo apt-get install pigpio python-pigpio python3-pigpio
```

## Repository and Code Structure
> File structure is not fully comphrehensive, only the most important folders and scripts are shown

    .
    ├── DMT_Arduino/                              
    │   ├── Dye_Injection_microcontroller/         # Source code for Dye Injection control
    │   └── TB_microcontroller/                    # Source code for closed loop control of flow actuator valve and testbed sync
    ├── DMT_RPi/                                   # Contains both required Pico Software Development Kit (SDK) and custom source code
    │   └── launcher.sh                            # Starting script for Raspberry Pi logging 
    ├── DMT_STM32/                                
    │   ├── DAQ_microcontroller/                   # Controls Pico Datalogger through Raspberry Pi
    │   │   └── Core/                       
    │   │      └── main.c                          # Source code for STM32 DAQ, contains communication protocols
    │   └── PIV_microcontroller/                   # Sends PIV signals to Raspberry Pi
    │   │   └── Core/                       
    │   │      └── main.c                          # Source code for STM32 DAQ, contains PIV protocols
    ├── client/                                    # JavaScript GUI
    ├── server/                                   
    │   ├── DAQ.py                                 # Main Python script if JavaScript GUI is to not be used
    │   ├── Module.py                              # List of required modules for program to run 
    │   ├── server_config.py                       # Default configuration when using DAQ.py 
    │   └── server.py                              # Flask API   
    ├── .gitignore
    ├── DMT Branch Strategy.drawio
    └── README.md

### Code Structure

The code was split into 4 parts:

* The data transmission circuit and actuators (under `DMT_Arduino/`, `DMT_RPi/`, `DMT_STM32/`)
* The Pico Data Logger (under `DMT_RPi/`) 
* The GUI interface (under `client/`)
* Python Backbones (under `server/`)

The associated folders are flashed on to the corresponding microcontrollers (Arduino TB, Arduino Dye Inject, DAQ STM32, PIV STM32 and Raspberry Pi)

## Getting Started

The first step for running the data acquisition process is to initialise the Raspberry Pi. The Raspberry Pi controls the Pico Datalogger and receives GPIO inputs from testbed components. 

### Starting the Raspberry Pi subassembly

Firstly, go to the relevant directory on the Raspberry Pi

```
$ cd DMT16_DAQ/DMT_RPi
```

Launch the launcher file:

```
$ sh launcher.sh
```

The next step is to run the software package on the Central PC. 

### Starting the Central PC

Ensure that the two USBs are connected through a hub to the PC. Make sure that you know which one is which. 
There are **TWO methods** to start the data acquisition system and electronics, one uses a JavaScript interface, the other uses a Python interface. 
Ensure that the CORS Chrome extension is on (this should be installed beforehand, refer to the prerequisites)

#### Using the JavaScript Interface

The JavaScript interface relies on a React Flask API. To launch the React frontend (i.e., the client), in the terminal, enter the following commands. 

```
cd client 
yarn start
```

This should open up to a landing page on Chrome on `localhost:3000` like this:

<img width="900" alt="Screenshot 2023-05-23 at 15 16 58" src="https://github.com/nk965/DMT16_DAQ/assets/107625806/904335f9-81fd-4e0c-a997-51b26524f464">

Then, in a new terminal on VS Code, start the Python Flask API using the follow commands and it will open on `localhost:5000`:

```
cd server
python3 server.py
```
> Alternatively, if `python3 server.py` does not work, use `python server.py` or `py server.py` commands 

An example of how to do this: 

![ezgif com-gif-maker](https://github.com/nk965/DMT16_DAQ/assets/107625806/fe8fe906-b167-4e40-8c1e-27567d5accd7)


##### Running the experiment

To run or start an experiment with custom configurations: 
* Click on *"Find Serial Ports"* and input the respective ports into the system
* Input desired characteristics
* Click on Reset Dye Injection System if required
* Click on Load User Configuration

To Adjust Transient Conditions:
* Click on the Transient tab
* Input as necessary, and load

To start:
* Click on Start Experiment 


#### Using the Python Interface

If you are using the Python interface, ensure to check the configuration file in `server/server_config.py` to input experiment conditions, as shown below.

<img width="926" alt="Screenshot 2023-05-23 at 17 06 28" src="https://github.com/nk965/DMT16_DAQ/assets/107625806/e10c857a-caf9-4a81-ab9d-75eeb01e25f6">


Then, run the Python script `server/DAQ.py`. 

By default, the bench scale tests `TB_TESTING`, `DAQ_TESTING` are commented out as well as `resetDyeInjection` 
To enable, uncomment the desired function, in the `server/DAQ.py` file. 

```python
    # logs = TB_TESTING(ports_available[TB_port_index], inputInfo) # Benchscale Test for TB system
    # logs = DAQ_TESTING(ports_available[DAQ_port_index], inputInfo) # Benchscale Test for DAQ system
    # logs = resetDyeInjection(ports_available[TB_port_index])

    logs = run(ports_available[DAQ_port_index], ports_available[TB_port_index])
```

## System Design

Below we will cover the rough groundwork, consisting of 5 microcontrollers. 

### Layout Structure

The main schematic for the communications between the components is as follows: 

<img width="1024" alt="Screenshot 2023-05-23 at 17 05 53" src="https://github.com/nk965/DMT16_DAQ/assets/107625806/dd334260-f5b7-45cc-af7a-ccb62c601bf7">

A list of commands used for the communication protocol is below, found in the `commands.py` file under server, and is referenced in the microcontrollers. 

[Data Acquisition Plan Final.docx](https://github.com/nk965/DMT16_DAQ/files/11546125/Data.Acquisition.Plan.Final.docx)

### Operating Sequence

The system of 5 microcontrollers allow us to control the timings and procedures precisely. 
<img width="542" alt="Screenshot 2023-05-23 at 16 56 16" src="https://github.com/nk965/DMT16_DAQ/assets/107625806/c52daa46-2fce-46d1-9f5e-4ac2c1b2ee5f">

### Dye Injection Control



### Flow Valve Control

In order to meet the requirements of transient boundary conditions (i.e. controlling the flow in the branch pipe during the experiment), we decided to use a digital PID controller. This was because incorporating an analog one without proper analog feedback would have been very hard. Furthermore, the use of a servomotor would have made this very difficult to control with a microcontroller. Finally, due to how low our sampling speed was, it would have been difficult to get a good step response from approximating the system as a continuous time system.

Thus, we used an implementation of a digital PID by applying the Bilinear Transform on the analog PID transfer function:

**The Bilinear Transform**
$$s = \frac{2}{T}\frac{z-1}{z+1}$$

Applying this on the general PID controller transfer function

**PID Controller**
$$H\left( s \right) = K_{P}+\frac{K_{I}}{s} + K_{D}s$$

We get the desired digital filter:

**Digital PID Controller**
$$y[n] = y[n-2] + \left( K_{P} + \frac{K_{I}T}{2} + \frac{2K_{D}}{T} \right)x[n] + \left( K_{I}T - \frac{4K_{D}}{T} \right)x[n-1] + \left( -K_{P} + \frac{K_{I}T}{2} + \frac{2K_{D}}{T} \right)x[n-2]$$


