from flask import Flask, request
import json
from DAQ import run, DAQ_TESTING, TB_TESTING

app = Flask(__name__)

def cleanInputs(dictionary):

    convertedConfig = {}

    for key, value in dictionary.items():

        if value.isdigit():

            convertedConfig[key] = float(value)

        elif value.lower() == "true":

            convertedConfig[key] = True

        elif value.lower() == "false":

            convertedConfig[key] = False

        else:

            convertedConfig[key] = value

    return convertedConfig

@app.route('/inputs', methods=['GET', 'POST'])
def inputs():

    if request.method == 'POST':
        print("POST")
        byte_string = request.data

        data_str = byte_string.decode('utf-8')

        params_dict = json.loads(data_str)

        print(params_dict)

        # object_methods = [method_name for method_name in dir(request)
        #           if callable(getattr(request, method_name))]

        # print(object_methods)

        # print(request.get_json())

        # req_data = request.get_json()

        # print(req_data)

    if request.method == 'GET':

        print("GET")

        # req_data = request.get_json()

        # print(req_data)

    return {'message': 'Success', 'data': '1§'}


if __name__ == '__main__':
    app.run(debug=True)
