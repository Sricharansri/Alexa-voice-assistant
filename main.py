from flask import Flask, render_template, request, redirect
import alexa

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/run', methods=['POST'])
def run():
    url = alexa.run_alexa()
    if url:
        return redirect(url)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
