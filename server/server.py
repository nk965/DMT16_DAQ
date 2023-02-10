from flask import Flask, request, json

app = Flask(__name__)

@app.route('/inputs', methods=['GET', 'POST'])
def inputs():
    return {"data": ["Member1", "Member2", "Member3"]}

@app.route('/inputs/userConfig', methods=['POST'])
def userConfig():
    request_data = json.load(request.data)
    print(request_data)

if __name__ == '__main__':
    app.run(debug=True)
