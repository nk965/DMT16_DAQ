from flask import Flask, request
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
    
    print("Hello World")

    return {'message': 'Success', 'data': '1§'}


if __name__ == '__main__':
    app.run(debug=True)
