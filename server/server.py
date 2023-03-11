from flask import Flask, request
import json
from helpers import cleanInputs
from DAQ import run, DAQ_TESTING, TB_TESTING
from server_config import inputInfo

app = Flask(__name__)

@app.route('/StartExperiment', methods=['POST'])
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

    # logs = run(inputs['DAQ_port'], inputs['TB_port'], inputs)

    print(inputs)

    # print(logs)

    return {'message': f"Experiment Started with {inputs}"}

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
