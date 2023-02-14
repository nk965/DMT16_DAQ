from flask import Flask, request, json

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
    return {"data": ["Member1", "Member2", "Member3"]}

@app.route('/inputs/userConfig', methods=['POST'])
def userConfig():
    request_data = json.load(request.data)
    print(request_data)

if __name__ == '__main__':
    app.run(debug=True)
