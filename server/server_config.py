"""
@author: Nicholas Kwok
Configuration file for sending user inputs into the microcontrollers
"""

inputInfo = {
    "syrLen": {
        "defaultValue": 150,
        "type": float,
        "range": [50, 500],
        "bits": 8,
        "units": "mm",
        "submission_form": "userConfig"
    },
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
        "defaultValue": 10,
        "type": float,
        "range": [0, 800],
        "bits": 16,
        "units": "s",
        "submission_form": "userConfig"
    },
    "PIVfreq": {
        "defaultValue": 10,
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
        "defaultValue": 1.2,
        "type": float,
        "range": [0, 10],
        "bits": 8,
        "units": "s",
        "submission_form": "userConfig"
    },
    "dutyCycle": {
        "defaultValue": 0.4,
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
        "bits": None,
        "units": "%", #TODO: use units of momentum ratio?
        "submission_form": "transientInput"
    },
    "end_y": {
        "defaultValue": 55,
        "type": float,
        "range": [0, 100],
        "bits": None,
        "units": "", #TODO: use units of momentum ratio?
        "submission_form": "transientInput"
    },
    "nodes": {
        "defaultValue": 7,
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
        "defaultValue": 15,
        "type": float,
        "range": [0, 800],
        "bits": None,
        "units": "",
        "submission_form": "transientInput"
    },
}
