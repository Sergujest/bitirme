import pymongo
from datetime import datetime as dt
import bson.objectid as oID
import QuestionClass
import LikeClass

myclient = pymongo.MongoClient("mongodb://localhost:27017/",maxPoolSize=None)
projectDB=myclient['Q&A_Video']
questionCol=projectDB['questions']

class Answer:
    def __init__(self,userID,userMail,detail,isTeacher,point=0,likes=[],_id=None):
        self._id=oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        self.userID=oID.ObjectId(userID) if(type(userID)!=oID.ObjectId) else userID
        self.userMail=userMail
        self.detail=detail
        self.point=point
        self.likes=likes
        self.isTeacher=isTeacher
    
    def printQuestion(self):
        print(self.__dict__)

    def insertAnswerByQuestionID(self,questionID):
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        questionCursor=questionCol.find({'$or':[\
            {'_id':questionID,'answers._id':self._id},
            {'_id':questionID,'answers.userID':self.userID}
            ]})
        if(questionCursor.count()==0):
            questionCol.update({'_id':questionID},{'$push':{'answers':self.__dict__}})
            return 'Worked'
        else:
            return 'There is an Answer with this userID or _id'

    def updateAnswerDetailByQuestionID(self,questionID):
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        questionCol.update({'_id':questionID,'answers._id':self._id},{'$set':{'answers.$.detail':self.detail}})
        

    @staticmethod
    def deleteAnswerByIDAndQuestionID(_id,questionID):
        _id=oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        questionCol.update({'_id':questionID},{'$pull':{'answers':{'_id':_id}}})

    @staticmethod
    def getAnswersByAnswersCursor(answerCursor):
        answerList=[]
        for answer in answerCursor:
            likeList=LikeClass.Like.getLikesByLikesCursor(answer['likes'])
            answerList.append(Answer(answer['userID'],answer['userMail'],answer['detail'],answer['isTeacher'],answer['point'],likeList,answer['_id']))
        return answerList
    





