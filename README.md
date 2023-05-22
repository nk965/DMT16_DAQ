# Design Make and Test Group 16 (Electronics)
> Members of Electronics Group: Pike Amornchat, Nicholas Kwok, Jimmy van de Worp

> Supervisors: Dr Mike Bluck, Dr Matthew Eaton, Dr Antonis Sergis, Prof Yannis Hardalupas
## Project Brief

The mixing of hot and cold fluids in a T-junction is a scenario that is present in nuclear power plants, particularly between the intersection of the Reactor Pressure Vessel (RPV), Steam Generator (SG) and Pressuriser (PRZ) in a Pressurised Water Reactor (PWR). 

A well-known issue with T-junctions in PWRs is thermal fatigue phenomena. Previous failures include pipe ruptures in Japan and France mainly due to temperature fluctuations in the T-junctions causing high cycle thermal fatigue. 

In this super project, the intention is to design, make and test an experimental nuclear thermal-hydraulic rig (able to fit on a table) to both quantitatively and qualitatively characterise fluid flow in a transparent section and transient heat transfer effects in a stainless-steel opaque section. 

Experimental data from thermocouples will be captured through a data acquisition software and compared to Computational Fluid Dynamics (CFD) models. 

The wider test bed rig, which consists of all necessary ancillary subassemblies to precisely control temperature and flow rate, will be closely integrated with the transparent and opaque section in a way such that the experimentalist can easily switch in and out sections. 

The super project is the start of a wider initiative to understand the transient thermo-fluid induced stresses in a T-junction more comprehensively, and a key objective of this project is to provide extensibility of the platform so that future research into continuous health monitoring (CHM) and non-destructive evaluation (NDE) methods can be conducted.

In summary, the rig's primary goal is:
* Understand the fluid mechanics and thermal fatigue phenomena in a T-junction and provide future extensibility for research into CHM and NDE methods.
* Validation of CFD results from test data obtained.
* A novel platform to train both undergraduates and postgraduates on thermal hydraulic diagnostics.

## The aim of this subgroup - DMT16 DAQ

More specifically, this section of the group was created to deal with the wide range of electronic demands of the project. 

The main tasks were:
* To produce an intuitive GUI which allowed the user to control the initial conditions and boundary conditions
* To install and synchronise all of the measurements such that a time reference can be assigned to each measurement
* To control the actuators in order to produce the desired transient boundary conditions

# Getting Started

### Repository File Structure

    .
    ├── DMT_Arduino/                 # Compiled files (alternatively `dist`)
    │   ├── Dye_Injection_microcontroller
    │   └── TB_microcontroller 
    ├── DMT_RPi/                     # Documentation files (alternatively `doc`)
    ├── DMT_STM32/                   # Source files (alternatively `lib` or `app`)
    │   ├── DAQ_microcontroller
    │   └── PIV_microcontroller 
    ├── client/                      # Automated tests (alternatively `spec` or `tests`)
    ├── server/                      # Tools and utilities
    ├── .gitignore
    ├── DMT Branch Strategy.drawio
    └── README.md


> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`


## Prerequisites

Hello 

### Code Structure

The code was split into 3 parts:

* The data transmission circuit and actuators
* The PICO Data logger
* The GUI interface

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


