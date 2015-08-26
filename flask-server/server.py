import os, sys
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
import subprocess
from subprocess import call
from pymongo import MongoClient

base_path = os.path.dirname(__file__)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(base_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'gif'])
data_mapping_file = '/opt/omron/NameLabelMap.dat'
omron_training_data = '/opt/omron/OmronTrainingData'

@app.route('/face_rec', methods=['GET', 'POST'])
def face_rec():
    if request.method == 'POST':
        img = request.files['file']
        if img and allowed_file(img.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
            img.save(file_path)

        res = omron_rec(file_path)
        return jsonify(res)

@app.route('/imdb/<index>', methods=['GET'])
def imdb_data(index):
    client = MongoClient('10.116.66.16', 27017)
    db = client.face_demo
    collection = db.celebrities_new

    res = collection.find_one({"idx": int(index)})
    client.close()
    del res['_id']
    print res
    return jsonify(res)

###### Function Define ######
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def omron_rec(img_path):
    print img_path
    cmd = ['/opt/omron/vision_face', img_path, data_mapping_file, omron_training_data]
    cmd = ' '.join(cmd)
    res = run(cmd)
    print res
    res = {'name': "Sean_Chuang", 'Email': "sean_chuang@htc.com", 'xxx': "OOO"}
    remove(img_path)
    return res

def remove(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass

def run(cmd, need_return=False):
    print "run the cmd => " + cmd
    if need_return:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()
    print '------- run cmd end ------'
    out1, err1 = p.communicate()

    if need_return:
        result = out1.decode()
    else:
        result = "" 

    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)


###### Test #######
# curl -F "file=@test.jpg;" http://localhost:8888/face_rec
# {
#   "Email": "sean_chuang@htc.com",
#   "name": "Sean_Chuang",
#   "xxx": "OOO"
# }