from flask import Flask, request, render_template, redirect, Response
from subprocess import PIPE, run
import flask
import os
from werkzeug import secure_filename
UPLOAD_FOLDER = '/tmp/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def api_root():
    return render_template('index.html', val="")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    name = ""
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                name = ""
            else:
                # f.save(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = f.filename
        else:
            name = ""
        print(name)
        # cmd_list = ["pwd", "ls -l " + os.path.join(app.config['UPLOAD_FOLDER'], name)]
        cmd_list = ["clang " + os.path.join(app.config['UPLOAD_FOLDER'], name) + " -fopenmp -fsanitize=thread -fPIE -pie -g -o myApp","./myApp "]
        for cmd in cmd_list:
            arr = cmd.split()
            result = run(arr, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            if(result.returncode == 1):
                str = result.stderr
            else:
                str = result.stdout
        if request.args.get('type') == 'json':
            return flask.make_response(
                    flask.jsonify({'res': str}), 200)
        else:
            return render_template('index.html', val=str.split('\n'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
