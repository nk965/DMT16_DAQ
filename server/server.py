from flask import Flask, request, jsonify

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
    
    #print(request.form)

    #content = request.json['body']
    # Do something with the content received from the React app
    # For example, you can print it to the console or save it to a database

    #print(content)

    return {"test": "1", "test": "2"}


if __name__ == '__main__':
    app.run(debug=True)
