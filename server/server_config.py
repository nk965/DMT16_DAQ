"""
@author: Nicholas Kwok
Configuration file for sending user inputs into the microcontrollers
"""

inputInfo = {
    "syrDia": {
        "defaultValue": 30,
        "type": float,
        "range": [10, 50],
        "bits": 8,
        "units": "mm",
        "submission_form": "userConfig"
    },
    "dyeSpeed": {
        "defaultValue": 8,
        "type": float,
        "range": [0, 50],
        "bits": 16,
        "units": "mm/s",
        "submission_form": "userConfig"
    },
    "enPulse": {
        "defaultValue": True,
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
        "defaultValue": 15,
        "type": float,
        "range": [0, 800],
        "bits": 16,
        "units": "s",
        "submission_form": "userConfig"
    },
    "PIVfreq": {
        "defaultValue": 20,
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
        "defaultValue": 0.5,
        "type": float,
        "range": [0, 100],
        "bits": 16,
        "units": "s",
        "submission_form": "userConfig"
    },
    "dutyCycle": {
        "defaultValue": 0.30,
        "type": float,
        "range": [0, 1],
        "bits": 8,
        "units": "%",
        "submission_form": "userConfig"
    },
    "start_y": {
        "defaultValue": 25,
        "type": float,
        "range": [0, 100],
        "bits": 8,
        "units": "%", #TODO: use units of momentum ratio?
        "submission_form": "transientInput"
    },
    "end_y": {
        "defaultValue": 55,
        "type": float,
        "range": [0, 100],
        "bits": 8,
        "units": "", #TODO: use units of momentum ratio?
        "submission_form": "transientInput"
    },
    "nodes": {
        "defaultValue": 5,
        "type": float,
        "range": [0, 500],
        "bits": None,
        "units": "",
        "submission_form": "transientInput"
    },
    "presetConfig": {
        "defaultValue": "Linear",
        "type": str,
        "range": None,
        "bits": None,
        "units": "",
        "submission_form": "transientInput"
    },
    "trans_time": {
        "defaultValue": 4,
        "type": float,
        "range": [0, 800],
        "bits": 16,
        "units": "",
        "submission_form": "transientInput"
    },
    "stabilising_delay": {
        "defaultValue": 5,
        "type": float,
        "range": [0, 2000],
        "bits": 8,
        "units": "s",
        "submission_form": None
    },
    "branch_temp": {
        "defaultValue": 80,
        "type": float,
        "range": [30, 100],
        "bits": 16,
        "units": "C",
        "submission_form": None
    },
    "vol_inject": {
        "defaultValue": 20,
        "type": float,
        "range": [0, 100],
        "bits": 8,
        "units": "ml",
        "submission_form": None
    },
    "inject_time": {
        "defaultValue": 5, # this was 9 
        "type": float,
        "range": [0, 480],
        "bits": 8,
        "units": "s",
        "submission_form": None # TODO
    },
}
