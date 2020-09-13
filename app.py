from flask import Flask, render_template, request, url_for, flash, redirect 
import json
import os
import shutil
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'taran'
print(" Please open URL in browser http://<jenkins-server-ip:5000 ")
path="./static/file/test.json"






def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def copyFile():
    x = datetime.datetime.now()
    dt=x.strftime("%d-%m-%Y-%H-%M")
    source = path
    target = path+dt


# adding exception handling
    try:
        shutil.copy(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())

def move(jsondata):
    f = open(path, "w")
    f.write(jsondata)
    f.close()

def validateJson(jsondata):
    try:
        json.loads(jsondata)
    except ValueError as err:
        return False
    return True

@app.route('/thankyou')
def closeflask():
    shutdown_server()
    return render_template('submit.html')

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        title = request.form['w3review']
        status = validateJson(title)
        if status is True:
            copyFile()
            move(title)
            return redirect(url_for('closeflask'))
        else:
            flash('Json is not validate. It is been reseted default value')
            return redirect(url_for('index'))
        
    return render_template('index.html', filename=path)




