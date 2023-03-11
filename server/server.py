from flask import Flask, request
import json
from helpers import cleanInputs
from DAQ import run, DAQ_TESTING, TB_TESTING

app = Flask(__name__)

@app.route('/StartExperiment', methods=['POST'])
def StartExperiment():

    userConfig = globals().get('userConfig')

    transientInput = globals().get('transientInput')

    if userConfig is None:
        # Handle case where user config is not present
        return {'message': 'User Configuration Not found! Loading Defaults'}

    if transientInput is None:

        

        return {'message': 'Transient Configuration Not Found! Loading Defaults'}

    inputs = userConfig | transientInput

    run(inputs['DAQ_port'], inputs['TB_port'], inputs)
    print(run)

    return {'message': "Experiment Started"}

@app.route('/LoadTransConfig', methods=['POST'])
def LoadTransConfig():

    byte_string = request.data

    data_str = byte_string.decode('utf-8')

    transientInput = json.loads(data_str)

    globals()['transientInput'] = transientInput

    return {'message': 'Custom Transient Configuration Loaded'}

@app.route('/LoadUserConfig', methods=['POST'])
def LoadUserConfig():

    byte_string = request.data

    data_str = byte_string.decode('utf-8')

    userConfig = json.loads(data_str)

    globals()['userConfig'] = userConfig

    return {'message': 'Custom User Configuration Loaded'}

if __name__ == '__main__':
    app.run(debug=True)
