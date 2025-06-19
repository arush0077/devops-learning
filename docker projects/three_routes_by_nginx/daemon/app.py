from flask import Flask
app = Flask(__name__)

@app.route('/daemon/')
def daemon_index():
    return "Hello I am /daemon"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4090)
