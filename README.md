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

* VS Code (highly recommended) or suitable IDE (like PyCharm) - untested on Anaconda
* Please see `Modules.py` in `server/`
* MacOS or Windows

To run the JavaScript API:
* Check Installation Instructions

Optional (if you would like to edit and re-flash STM32 code):

* STM32 Cube MX
* STM32 Programmer
* STM32 IDE

## Repository and Code Structure
> File structure is not fully comphrehensive, only the most important folders and scripts are shown

    .
    ├── DMT_Arduino/                              
    │   ├── Dye_Injection_microcontroller         # Source code for Dye Injection control
    │   └── TB_microcontroller                    # Source code for closed loop control of flow actuator valve and testbed sync
    ├── DMT_RPi/                                  # Contains both required Pico Software Development Kit (SDK) and custom source code
    ├── DMT_STM32/                                
    │   ├── DAQ_microcontroller                   # Source code for STM32 DAQ - controls Pico Datalogger through Raspberry Pi 
    │   └── PIV_microcontroller                   # Source code for STM32 PIV - sends PIV signals to Raspberry Pi
    ├── client/                                   # JavaScript GUI
    ├── server/                                   
    │   ├── DAQ.py                                # Main Python script if JavaScript GUI is to not be used
    │   ├── Module.py                             # List of required modules for program to run 
    │   ├── server_config.py                      # Default configuration when using DAQ.py 
    │   └── server.py                             # Flask API   
    ├── .gitignore
    ├── DMT Branch Strategy.drawio
    └── README.md

### Code Structure

The code was split into 3 parts:

* The data transmission circuit and actuators (under `DMT_Arduino/`, `DMT_RPi/`, `DMT_STM32/`)
* The Pico Data Logger (under `DMT_RPi/`) 
* The GUI interface (under `client/`)
* Python Backbones (under `server/`)

The associated folders are flashed on to the corresponding microcontrollers (Arduino TB, Arduino Dye Inject, DAQ STM32, PIV STM32 and Raspberry Pi)

## Getting Started

Running Python r

## System Design

Below we will cover the rough groundwork

### Layout Structure

### Operating Sequence

put diagram here

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


