from app import flaskApp
from flask import request,render_template,redirect,jsonify,Flask, flash, url_for
import json
import bson.objectid as oID
from QuestionClass import Question
from AnswerClass import Answer
from LikeClass import Like
from UserClass import User
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/videos'
ALLOWED_EXTENSIONS = set(['mp4','png'])
flaskApp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@flaskApp.route('/teacher' , methods=['GET'])
def handleTeacher():
    try:
        #videoLink=request.args.get('userID')
        return render_template("public/teacher.html")
    except Exception as error:
        return str(error)


@flaskApp.route('/teachervideos' , methods=['GET','POST'])
def handleTeacherVideos():
    if(request.method=='POST'):
        try:
            questionID=request.args.get('userID')
            # check if the post request has the file part
            if 'file' not in request.files:
                for i in request.files:
                    print(i)
            file = request.files['file']
            print('teletabi')
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                print('no selected file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return 't'
            else:
                return 'k'
        except Exception as ex:
            print(str(ex))
            return 'k'
    else:
        try:
            userID=request.args.get('userID')
            user=User.getUserByID(userID)
            videos=user.videos
            titleList=[]
            for video in videos:
                titleList.append({'title':video})
            print('a')
            return json.dumps(titleList)
        except Exception as error:
            return str(error)


