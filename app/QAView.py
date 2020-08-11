from app import flaskApp
from flask import request,render_template,redirect,jsonify
import json
import bson.objectid as oID
from QuestionClass import Question
from AnswerClass import Answer
from LikeClass import Like
from UserClass import User


@flaskApp.route('/question' , methods=['GET','POST'])
def handleQuestion():
    if(request.method=='POST'):
        try:
            content=request.json
            userID=content['userID']
            if(User.checkUserByID(userID)==True):
                userMail=content['userMail']
                title=content['title']
                detail=content['detail']
                videoLink=content['videoLink']
                videoTime=content['videoTime']
                question=Question(userID,userMail,title,detail,videoLink,videoTime)
                response=question.insertQuestion()
                print(response)
                return response
            else:
                print('testere')
                return 'There is no User with this ID'
        except Exception as error:
            return str(error)
    
    else:
        try:
            videoLink=request.args.get('videoLink')
            videoTime=request.args.get('videoTime')
            questions=Question.getQuestionsByVideoAndTime(videoLink,videoTime)
            questionList=[]
            for question in questions:
                likes=question.likes
                likeList=[]
                for like in likes:
                    likeList.append(like.__dict__)
                questionDict={'_id':str(question._id),'userID':str(question.userID),'userMail':question.userMail,'title':question.title,\
                    'detail':question.detail,'videoTime':question.videoTime,'likes':likeList,'point':question.point,'answerCount':len(question.answers)}
                questionList.append(questionDict)
            return json.dumps(questionList)
        except Exception as error:
            return str(error)


@flaskApp.route('/answer' , methods=['GET','POST'])
def handleAnswer():
    if(request.method=='POST'):
        try:
            content=request.json
            userID=content['userID']
            if(User.checkUserByID(userID)==True):
                userMail=content['userMail']
                questionID=content['questionID']
                detail=content['detail']
                isTeacher=content['isTeacher']
                answer=Answer(userID,userMail,detail,isTeacher)
                response=answer.insertAnswerByQuestionID(questionID)
                print(response)
                return response
            else:
                return 'There is no User with this ID'
        except Exception as error:
            return str(error)
    
    else:
        try:
            questionID=request.args.get('questionID')
            question=Question.getQuestionsByQuestionID(questionID)
            answerList=[]
            answers=question.answers
            for answer in answers:
                print(answer.__dict__)
                likes=answer.likes
                likeList=[]
                for like in likes:
                    likeList.append(like.__dict__)
                answerDict={'_id':str(answer._id),'userID':str(answer.userID),'userMail':answer.userMail,\
                    'detail':answer.detail,'point':answer.point,'likes':likeList,'isTeacher':answer.isTeacher}
                answerList.append(answerDict)
            return json.dumps(answerList)
            
        except Exception as error:
            return str(error)

@flaskApp.route('/answerLike' , methods=['POST'])
def handleAnswerLike():
    try:
        content=request.json
        userID=content['userID']
        if(User.checkUserByID(userID)==True):
            questionID=content['questionID']
            answerID=content['answerID']
            like=Like(True,userID)
            response=like.insertLikeToAnswerByQuestionIDAndAnswerID(questionID,answerID)
            print(response)
            return response
        else:
            return 'There is no User with this ID'
    except Exception as error:
        return str(error)

@flaskApp.route('/questionLike' , methods=['POST'])
def handleQuestionLike():
    try:
        content=request.json
        userID=content['userID']
        if(User.checkUserByID(userID)==True):
            questionID=content['questionID']
            like=Like(True,userID)
            response=like.insertLikeToQuestionByQuestionID(questionID)
            print(response)
            return response
        else:
            return 'There is no User with this ID'
    except Exception as error:
        return str(error)