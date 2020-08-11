import pymongo
from datetime import datetime as dt
import bson.objectid as oID
import AnswerClass
import LikeClass

myclient = pymongo.MongoClient("mongodb://localhost:27017/",maxPoolSize=None)
projectDB=myclient['Q&A_Video']
questionCol=projectDB['questions']


class Question:
    def __init__(self,userID,userMail,title,detail,videoLink,videoTime,point=0,answers=[],likes=[],_id=None):
        self._id=oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        self.userID=oID.ObjectId(userID) if(type(userID)!=oID.ObjectId) else userID
        self.userMail=userMail
        self.title=title
        self.detail=detail
        self.videoLink=videoLink
        self.videoTime=int(videoTime)
        self.point=point
        self.answers=answers
        self.likes=likes
    
    def printQuestion(self):
        print(self.__dict__)

    def insertQuestion(self):
        try:
            questionCol.insert_one(self.__dict__)
            return 'Worked'
        except:
            return 'Insert Question Error'

    @staticmethod
    def getQuestionsByVideoAndTime(videoLink,videoTime):
        questions=questionCol.find({'videoLink':videoLink,'$and':[{'videoTime':{'$gte':int(videoTime)*60}},{'videoTime':{'$lt':(int(videoTime)+1)*60}}]})
        if(questions!=None):
            questionList=[]
            for question in questions:

                answerList=AnswerClass.Answer.getAnswersByAnswersCursor(question['answers'])
                
                likeList=LikeClass.Like.getLikesByLikesCursor(question['likes'])

                questionList.append(Question(question['userID'],question['userMail'],question['title'],question['detail'],question['videoLink']\
                    ,question['videoTime'],question['point'],answerList,likeList,question['_id']))
            return questionList
        else:
            return None

    @staticmethod
    def getQuestionsByQuestionID(questionID):
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        questionDoc=questionCol.find_one({'_id':questionID})
        if(questionDoc!=None):
            answerList=AnswerClass.Answer.getAnswersByAnswersCursor(questionDoc['answers'])
            
            likeList=LikeClass.Like.getLikesByLikesCursor(questionDoc['likes'])

            question=Question(questionDoc['userID'],questionDoc['userMail'],questionDoc['title'],questionDoc['detail'],questionDoc['videoLink']\
                        ,questionDoc['videoTime'],questionDoc['point'],answerList,likeList,questionDoc['_id'])
            return question
        else:
            return None

    @staticmethod
    def deleteQuestion(_id):
        questionCol.delete_one({'_id':_id})


    


#importAnswer()
#question=Question('5ef103f8a66227f98793587a','teletabi@mail','ali','veli','link','canik',5)
#question.insertQuestion()