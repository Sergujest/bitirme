import pymongo
from datetime import datetime as dt
import bson.objectid as oID


myclient = pymongo.MongoClient("mongodb://localhost:27017/",maxPoolSize=None)
projectDB=myclient['pyTrend']


def insertUserFormal(fName,sName,companyTitle,email,password):
    try:
        userCol=projectDB['users']
        userCol.insert_one({'firstName':fName,'surName':sName,'companyTitle':companyTitle,'mail':email,'password':password,'userType':'normal','registerDate':dt.utcnow(),'lastLogInDate':dt.utcnow()})
        return 'Worked'
    except:
        return 'Insert User Formal Error'
        

def insertUserGoogle(fName,googleID,email):
    try:
        googleUserCol=projectDB['googleIDs']
        googleUserCol.insert_one({'googleID':googleID})
        print(googleID)
        userID=googleUserCol.find_one({'googleID':googleID})['_id']
        userCol=projectDB['users']
        userCol.insert_one({'_id':userID,'firstName':fName,'mail':email,'userType':'google','registerDate':dt.utcnow(),'lastLogInDate':dt.utcnow()})
        return 'Worked'
    except:
        return 'Insert User Google Error'

def insertUserFacebook(facebookID):
    try:
        facebookUserCol=projectDB['facebookIDs']
        facebookUserCol.insert_one({'facebookID':facebookID})
        userID=facebookUserCol.find_one({'facebookID':facebookID})['_id']
        userCol=projectDB['users']
        userCol.insert_one({'_id':userID,'userType':'facebook','registerDate':dt.utcnow(),'lastLogInDate':dt.utcnow()})
        return 'Worked'
    except:
        return 'Insert User Facebook Error'

def getUserByMail(newMail):
        userCol=projectDB['users']
        return userCol.find_one({'mail':newMail})

def getUserIDByGoogleID(newID):
        googleUserCol=projectDB['googleIDs']
        return googleUserCol.find_one({'googleID':newID})

'''def findUserByFacebookID(newID):
    facebookUserCol=projectDB['facebookIDs']
    if(facebookUserCol.find_one({'facebookID':newID})==None):
        return False
    else:
        return facebookUserCol.find_one({'facebookID':newID})['_id']'''

def getUserByID(userID):
    if(type(userID)!=oID.ObjectId):
        userID=oID.ObjectId(userID)
    userCol=projectDB['users']
    return userCol.find_one({'_id':userID})

def updateUser(query,setValue):
    try:
        setDict={}
        setDict['$set']=setValue
        userCol=projectDB['users']
        if(type(query['_id'])!=oID.ObjectId):
            query['_id']=oID.ObjectId(query['_id'])
        userCol.update_one(query,setDict)
        return 'Worked'
    except:
        return 'Update User Error'
