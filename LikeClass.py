import pymongo
from datetime import datetime as dt
import bson.objectid as oID
import QuestionClass
import AnswerClass

myclient = pymongo.MongoClient("mongodb://localhost:27017/",maxPoolSize=None)
projectDB=myclient['Q&A_Video']
questionCol=projectDB['questions']

class Like:
    def __init__(self,value,userID,_id=None):
        self._id=oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        self.userID=oID.ObjectId(userID) if(type(userID)!=oID.ObjectId) else userID
        self.value=value

    def insertLikeToQuestionByQuestionID(self,questionID):
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        questionCursor=questionCol.find({'$or':[\
            {'_id':questionID,'likes._id':self._id},
            {'_id':questionID,'likes.userID':self.userID}
            ]})
        if(questionCursor.count()==0):
            questionCol.update({'_id':questionID},{'$push':{'likes':self.__dict__}})
            question=questionCursor=questionCol.find_one({'_id':questionID})
            newPoint=len(question['likes'])
            questionCol.update({'_id':questionID},{'$set':{'point':newPoint}})
            return 'Worked'
        else:
            return 'There is a Like with this userID or _id for this Question'
    
    def insertLikeToAnswerByQuestionIDAndAnswerID(self,questionID,answerID):
        answerID=oID.ObjectId(answerID) if (type(answerID)!=oID.ObjectId) else answerID
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        print(answerID)
        questionCursor=questionCol.find({'$or':[\
            {'_id':questionID,'answers._id':answerID,'answers.$.likes._id':self._id},
            {'_id':questionID,'answers._id':answerID,'answers.$.likes.userID':self.userID}
            ]})
        if(questionCursor.count()==0):
            questionCol.update({'_id':questionID,'answers._id':answerID},{'$push':{'answers.$.likes':self.__dict__}})
            question=questionCursor=questionCol.find_one({'_id':questionID})
            for answer in question['answers']:
                if(answer['_id']==answerID):
                    newPoint=len(answer['likes'])
            questionCol.update({'_id':questionID,'answers._id':answerID},{'$set':{'answers.$.point':newPoint}})
            return 'Worked'
        else:
            return 'There is a Like with this userID or _id for this Answer'

    def updateQuestionLikeByQuestionID(self,questionID):
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        questionCol.update({'_id':questionID,'likes._id':self._id},{'$set':{'likes.$.value':self.value}})

    def updateAnswerLikeByQuestionIDAndAnswerID(self,questionID,answerID):
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        answerID=oID.ObjectId(answerID) if (type(answerID)!=oID.ObjectId) else answerID
        questionCol.update_one(\
            {'_id':questionID,'answers._id':answerID,'answers.likes._id':self._id},
            {'$set':{'answers.$.likes.$[element].value':self.value}},
            array_filters=[ { 'element._id': self._id }],
            upsert=True
            )

    @staticmethod
    def getLikesByLikesCursor(likeCursor):
        likeList=[]
        for like in likeList:
            likeList.append(Like(like['value'],like['userID'],answer['_id']))
        return likeList

    @staticmethod
    def deleteQuestionLikeByIDAndQuestionID(_id,questionID):
        _id=oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        questionCol.update({'_id':questionID},{'$pull':{'likes':{'_id':_id}}})

    @staticmethod
    def deleteAnswerLikeByIDQuestionIDAndAnswerID(_id,questionID,answerID):
        _id=oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        questionID=oID.ObjectId(questionID) if (type(questionID)!=oID.ObjectId) else questionID
        answerID=oID.ObjectId(answerID) if (type(answerID)!=oID.ObjectId) else answerID
        questionCol.update({'_id':questionID,'answers._id':answerID},{'$pull':{'answers.$.likes':{'_id':_id}}})
