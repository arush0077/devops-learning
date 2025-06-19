from flask import Flask
app = Flask(__name__)

@app.route('/app/')
def app_index():
    return "Hello I am /app"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
