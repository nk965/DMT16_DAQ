from flask import Flask, request, jsonify
import json
import numpy as np
from helpers import cleanInputs, linear_interpolation
from DAQ import run, resetDyeInjection, DAQ_TESTING, TB_TESTING
from PySerial import list_ports
from server_config import inputInfo

app = Flask(__name__)

@app.route('/StartExperiment', methods=['POST', 'GET'])
def StartExperiment():

    userConfig = globals().get('userConfig')

    transientInput = globals().get('transientInput')

    if userConfig is None:

        default_userConfig = {key: value["defaultValue"] for key, value in inputInfo.items() if value.get("submission_form") == "userConfig"}

        globals()['userConfig'] = default_userConfig

        return {'message': 'User Configuration Not found! Loading Defaults'}

    if transientInput is None:

        default_transientInput = {key: value["defaultValue"] for key, value in inputInfo.items() if value.get("submission_form") == "transientInput"}

        globals()['transientInput'] = default_transientInput

        return {'message': 'Transient Configuration Not Found! Loading Defaults'}

    inputs = userConfig | transientInput

    logs = run(inputs['DAQ_port'], inputs['TB_port'], inputs)

    # print(inputs)

    # print(logs)

    return {'message': {'inputs': inputs}}

@app.route('/ResetDyeInjection', methods=['GET', 'POST'])
def ResetDyeInjection():
    
    userConfig = globals().get('userConfig')

    if userConfig is None:

        default_userConfig = {key: value["defaultValue"] for key, value in inputInfo.items() if value.get("submission_form") == "userConfig"}

        globals()['userConfig'] = default_userConfig

        return {'message': 'User Configuration Not found! Loading Defaults'}

    inputs = userConfig

    logs = resetDyeInjection(inputs['TB_port'])

    return {'message': {'logs': logs}}


@app.route('/RefreshTransConfig', methods=['GET'])
def RefreshTransConfig():

    userConfig = globals().get('userConfig')

    transientInput = globals().get('transientInput')

    if userConfig is None:

        userConfig_trans_time = {'trans_time': inputInfo['trans_time']['defaultValue']}

        globals()['userConfig'] = userConfig_trans_time

        return {'message': 'Transient Time Not Loaded! Loading Defaults'}

    if transientInput is None:

        default_transientInput = {key: value["defaultValue"] for key, value in inputInfo.items() if value.get("submission_form") == "transientInput"}

        globals()['transientInput'] = default_transientInput

    graph_info = globals()['userConfig'] | globals()['transientInput']

    if graph_info['presetConfig'] == "Linear":

        labels, values = linear_interpolation(graph_info['start_y'], graph_info['end_y'], graph_info['nodes'], graph_info['trans_time'])

        labels = np.round(labels, decimals=3)
        values = np.round(values, decimals=3)

        return jsonify({'message': {'labels': labels.tolist(), 'values': values.tolist()}})

    return jsonify({'message': 'Configuration Not Found'})

@app.route('/FindPorts', methods=['GET'])
def FindPorts():

    ports_available = list_ports()

    ports = {}

    for port, index in enumerate(ports_available):
        ports[index] = port

    return ports

@app.route('/LoadTransConfig', methods=['POST'])
def LoadTransConfig():

    byte_string = request.data

    data_str = byte_string.decode('utf-8')

    transientInput = json.loads(data_str)

    globals()['transientInput'] = cleanInputs(transientInput)

    return {'message': 'Custom Transient Configuration Loaded'}

@app.route('/LoadUserConfig', methods=['POST'])
def LoadUserConfig():

    byte_string = request.data

    data_str = byte_string.decode('utf-8')

    userConfig = json.loads(data_str)

    globals()['userConfig'] = cleanInputs(userConfig)

    return {'message': 'Custom User Configuration Loaded'}

if __name__ == '__main__':
    
    app.run(debug=True)
