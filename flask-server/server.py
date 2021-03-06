import os
import sys
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
import subprocess
from pymongo import MongoClient
import json

base_path = os.path.dirname(__file__)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(base_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'gif'])

omron_album = '/opt/omron/celebrity_album'

client = MongoClient('10.116.66.16', 27017)


@app.route('/face_rec', methods=['GET', 'POST'])
def face_rec():
    if request.method == 'POST':
        img = request.files['file']
        img_name = to_utf8(img.filename)
        if img and allowed_file(img_name):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            img.save(file_path)

        res = omron_rec(file_path)
        return jsonify(res)


@app.route('/imdb/<index>', methods=['GET'])
def imdb_data(index):
    res = query_imdb(index)
    return jsonify(res)


# Function Define #
def query_imdb(index):
    db = client.face_demo
    collection = db.celebrities_new
    res = collection.find_one({"idx": int(index)})
    del res['_id']
    return res


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def omron_rec(img_path):
    print img_path
    cmd = [
        '/opt/omron/vision_face',
        img_path, omron_album]
    cmd = ' '.join(cmd)
    res = to_utf8(run(cmd, True))
    print res

    # from random import randint
    # person_idx = randint(1, 530) - 1
    # res = query_imdb(person_idx)

    # Example result #
    # res = 'cond:0.375;a:342;b:32;{\
    # "_id" : {\
    #     "$oid" : "55e3cf57f058500f9238f601"\
    # }, \
    # "title" : "VP", \
    # "department" : "U00000 MASD", \
    # "phone" : "28452", \
    # "name" : "Steve Wang", \
    # "location" : "Xindian TPE1 ", \
    # "idx" : 530\
    # }'

    remove(img_path)

    if res:
        others = res.split(';{')[0]
        json_data = '{' + res.split(';{', 2)[1]
        result = json.loads(json_data)
        for item in others.split(';'):
            key = item.split(':')[0]
            value = item.split(':')[1]
            result[key] = value
        return result
    else:
        return {}


def remove(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass


def to_utf8(text):
    if text:
        return text.encode('utf8', 'replace')
    else:
        return None


def run(cmd, need_return=False):
    print "run the cmd => " + cmd
    if need_return:
        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        result = out1.decode('utf8')
    else:
        result = ""

    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)


# Test #
# curl -F "file=@test.jpg;" http://localhost:8888/face_rec
# {
#   "Email": "sean_chuang@htc.com",
#   "name": "Sean_Chuang",
#   "xxx": "OOO"
# }