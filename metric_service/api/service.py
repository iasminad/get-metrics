# import flask module
from flask import Flask, jsonify, request, render_template

# instance of flask application
app = Flask(__name__)

latest_data = []

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route("/receive", methods=['POST'])
def receive():
    # global latest_data
    data = request.get_json()
    latest_data.append(data)
    return jsonify(data) 

@app.route("/show", methods=['GET'])
def show_data():
    if latest_data:
        return jsonify({"Data": latest_data})
    else:
        return jsonify({"message": "No data received yet"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)