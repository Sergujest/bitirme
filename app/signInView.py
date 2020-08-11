from app import flaskApp 
from flask import request,render_template,redirect,jsonify
from datetime import datetime as dt
import json
from auth import *
from UserClass import User

@flaskApp.route("/")
def index():
    return render_template("public/index.html")

@flaskApp.route("/sign_in",methods=['GET','POST'])
def sign_in():
    if(request.method=='POST'):
        content=request.json
        firstName=content['firstName']
        sName=content['surName']
        companyTitle=content['companyTitle']
        mail=content['mail']
        password=content['password']
        if(getUserByMail(mail)==None):
            response=insertUserFormal(firstName,sName,companyTitle,mail,password)
            if(response=='Worked'):
                userID=getUserByMail(mail)['_id']
                return str(userID)
            else:
                return 'Insert User Formal Error'
        else:
            return 'Used_Mail'
    return render_template("public/sign_in.html")

@flaskApp.route('/google_signIn', methods=['POST'])
def google_signIn():
    content=request.json
    name=content['firstName']
    mail=content['mail']
    token=content['id_token']
    googleID=google_authenticate(token)
    if(googleID=='error'):
        return 'error'
    else:
        user=User.getUserByGoogleID(googleID)
        if(user!=None):
            userID=user._id
            response=user.updateUserlastLogin()
            if(response=='Worked'):
                signInDict={'isSuccessful':'true','_id':str(userID),'mail':user.mail,'isTeacher':user.isTeacher}
                return json.dumps(signInDict)
            else:
                signInDict={'isSuccessful':'false'}
                return json.dumps(signInDict)
        else:
            newUser=User(name,mail,googleID)
            response=newUser.insertUser()
            if(response=='Worked'):
                user=User.getUserByGoogleID(googleID)
                signInDict={'isSuccessful':'true','_id':str(user._id),'mail':user.mail,'isTeacher':user.isTeacher}
                return json.dumps(signInDict)
            else:
                signInDict={'isSuccessful':'false'}
                return json.dumps(signInDict)




