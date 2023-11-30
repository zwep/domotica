from flask import Flask, render_template

app = Flask(__name__,  template_folder='templates')


@app.route('/plot')
def plot():
    return render_template('plot.html')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    import os
    print(os.getcwd())
    app.run()
