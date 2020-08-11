
import pymongo
from datetime import datetime as dt
import bson.objectid as oID

myclient = pymongo.MongoClient("mongodb://localhost:27017/",maxPoolSize=None)
projectDB=myclient['Q&A_Video']
userCol=projectDB['users']

class User:
    def __init__(self,name,mail,googleID,_id=None,registerDate=dt.utcnow(),lastLoginDate=dt.utcnow(),isTeacher=False,videos=[]):
        self._id=oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        self.name=name
        self.mail=mail
        self.registerDate=registerDate
        self.lastLoginDate=lastLoginDate
        self.isTeacher=isTeacher
        self.googleID=googleID
        self.videos=videos
    
    def printUser(self):
        print(self.__dict__)

    def insertUser(self):
        try:
            userCol.insert_one({'name':self.name,'mail':self.mail,'isTeacher':self.isTeacher,\
                'videos':self.videos,'googleID':self.googleID,'registerDate':self.registerDate,'lastLoginDate':self.lastLoginDate})
            return 'Worked' 
        except:
            return 'Error Insert User'

    def deleteUser(self):
        userCol.delete_one({'_id':self._id})

    def updateUserlastLogin(self):
        try:
            userCol.update_one({'_id':self._id},{'$set':{'lastLoginDate':dt.utcnow()}})
            return 'Worked'
        except:
            return 'Update User Error'


    @staticmethod
    def getUserByID(_id):
        _id= oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        user=userCol.find_one({'_id':_id})
        if(user!=None):
            newUser=User(user['name'],user['mail'],user['googleID'],user['_id'],user['registerDate'],user['lastLoginDate'],user['isTeacher'],user['videos'])
            return newUser
        else:
            return None

    @staticmethod
    def getUserByGoogleID(googleID):
        user=userCol.find_one({'googleID':googleID})
        if(user!=None):
            newUser=User(user['name'],user['mail'],user['googleID'],user['_id'],user['registerDate'],user['lastLoginDate'],user['isTeacher'],user['videos'])
            return newUser
        else:
            return None
    
    @staticmethod
    def checkUserByID(_id):
        _id= oID.ObjectId(_id) if(type(_id)!=oID.ObjectId) else _id
        user=userCol.find_one({'_id':_id})
        if(user!=None):
            return True
        else:
            return False
    
