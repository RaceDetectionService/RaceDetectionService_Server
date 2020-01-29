
from flask import Flask, request, render_template, redirect
from subprocess import PIPE, run
from werkzeug import secure_filename
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        # cmd_list = ["clang DRB001-antidep1-orig-yes.c -fopenmp -fsanitize=thread -fPIE -pie -g -o myApp", "./myApp "]
        cmd_list = ["pwd", "ls -l"]
        for cmd in cmd_list:
            arr = cmd.split()
            result=run(arr, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            if(result.returncode == 1):
                str = result.stderr
            else:
                str = result.stdout
            print(str)
        return render_template('index.html', val=str.split('\n'))
    else:
        return render_template('index.html', val="")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template('upload.html')


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)