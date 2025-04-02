from flask import Flask, g

DATABASE = 

app = Flask(__name__)

@app.route('/')
def home():
    #Home Page
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)