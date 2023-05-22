# Design Make and Test Group 16

## Project Brief

The aim of this project is..

* Produce a test rig capable of measuring..
* Compare the measured results to CFD to verify the simulations

## The aim of this subgroup - DMT16 DAQ

Our subgroup was created in order to deal with the wide range of electronic demands of the project. The main tasks were:

* To produce an intuitive GUI which allowed the user to control the initial conditions and boundary conditions
* To install and synchronise all of the measurements such that a time reference can be assigned to each measurement
* To control the actuators in order to produce the desired transient boundary conditions

# Getting Started

text here

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
$$y[n]-y[n-2]= \left(  \right)x[n] + \left( s \right)x[n-1] + \left( s \right)x[n-2]$$

**The Cauchy-Schwarz Inequality**
$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$


