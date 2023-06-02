"""
@author: Nicholas Kwok
Configuration file for sending user inputs into the microcontrollers
"""

inputInfo = {
    "DAQ_port": {
        "defaultValue": "COM7",
        "submission_form": "userConfig"
    },
    "TB_port": {
        "defaultValue": "COM8",
        "submission_form": "userConfig"
    },
    "syrDia": {
        "defaultValue": 29.5,
        "type": float,
        "range": [10, 35],
        "bits": 8,
        "units": "mm",
        "submission_form": "userConfig"
    },
    "enPulse": {
        "defaultValue": False,
        "type": bool,
        "range": None,
        "bits": 8,
        "units": None,
        "submission_form": "userConfig"
    },
    "testDelay": {
        "defaultValue": 60,
        "type": float,
        "range": None,
        "bits": None,
        "units": "s",
        "submission_form": "userConfig"
    },
    "lenExperiment": {
        "defaultValue": 60, # put this for Opaque test
        "type": float,
        "range": [0, 800],
        "bits": 16,
        "units": "s",
        "submission_form": "userConfig"
    },
    "PIVfreq": {
        "defaultValue": 6,
        "type": float,
        "range": [5, 50000], #TODO check with Pike with this
        "bits": 16,
        "units": "Hz",
        "submission_form": "userConfig"
    },
    "Datafreq": {
        "defaultValue": 200,
        "type": float,
        "range": [100, 5000],
        "bits": 8,
        "units": "ms",
        "submission_form": "userConfig"
    },
    "cyclePeriod": {
        "defaultValue": 2, # 2 or 3
        "type": float,
        "range": [0, 100],
        "bits": 16,
        "units": "s",
        "submission_form": "userConfig"
    },
    "dutyCycle": {
        "defaultValue": 0.8, #0.5 or 0.8
        "type": float,
        "range": [0, 1],
        "bits": 8,
        "units": "%",
        "submission_form": "userConfig"
    },
    "start_y": {
        "defaultValue": 26.232, #1: 32.116, #2: 26.223, #3: 20.312
        "type": float,
        "range": [0, 33], # remember 65.535
        "bits": 16, 
        "units": "ml/s", #TODO: use units of momentum ratio?
        "submission_form": "transientInput"
    },
    "end_y": {
        "defaultValue": 30, #1: who cares, #2: 30, #3: who cares 
        "type": float,
        "range": [0, 33], #remember 65.535
        "bits": 16,
        "units": "", #TODO: use units of momentum ratio?
        "submission_form": "transientInput"
    },
    "nodes": {
        "defaultValue": 1500, 
        "type": float,
        "range": [0, 500],
        "bits": None,
        "units": "",
        "submission_form": "transientInput"
    },
    "presetConfig": {
        "defaultValue": "Step", #1: Constant, #2: Linear, #3: Sine
        "type": str,
        "range": None,
        "bits": None,
        "units": "",
        "submission_form": "transientInput"
    },
    "trans_time": {
        "defaultValue": 40, # trans_time is 30 for Opaque
        "type": float,
        "range": [0, 800],
        "bits": 16,
        "units": "",
        "submission_form": "userConfig"
    },
    "stabilising_delay": {
        "defaultValue": 2,
        "type": float,
        "range": [0, 2000],
        "bits": 8,
        "units": "s",
        "submission_form": "userConfig"
    },
    "branch_temp": {
        "defaultValue": 30,
        "type": float,
        "range": [30, 100],
        "bits": 16,
        "units": "C",
        "submission_form": "userConfig"
    },
    "vol_inject": {
        "defaultValue": 30,
        "type": float,
        "range": [0, 100],
        "bits": 8,
        "units": "ml",
        "submission_form": "userConfig"
    },
    "inject_time": {
        "defaultValue": 40, # for Opaque
        "type": float,
        "range": [0, 480],
        "bits": 8,
        "units": "s",
        "submission_form": "userConfig"
    },
    "frequency": {
        "defaultValue": 2, # Only #3 
        "type": float,
        "range": [0, 20],
        "bits": 8,
        "units": "Hz",
        "submission_form": "None"
    },
    "amplitude": {
        "defaultValue": 15, # Only #3
        "type": float,
        "range": [0, 1000],
        "bits": 8,
        "units": "s",
        "submission_form": "None"
    },
    "step_time": {
        "defaultValue": 7, # this was 9 
        "type": float,
        "range": [0, 800],
        "bits": 8,
        "units": "s",
        "submission_form": "None"
    },
    "step_value": {
        "defaultValue": 5.893, # this was 9 
        "type": float,
        "range": [0, 1000],
        "bits": 8,
        "units": "",
        "submission_form": "None"
    },
}
