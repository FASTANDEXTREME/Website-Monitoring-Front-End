from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')  

@app.route('/info')
def info():
    return render_template('info.html')  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7071)