from app import flaskApp
from flask import request,render_template,redirect,jsonify
import json
import bson.objectid as oID


@flaskApp.route('/videos' , methods=['GET'])
def handleVideo():
    '''if(request.method=='POST'):
        content=request.json
        userID=content['userID']
        trendName=content['trendName']
        groupName=content['groupName']
        keyword=content['keyword']
        startDate=content['startDate']
        endDate=content['endDate']
        horizon=content['horizon']
        language=content['language']
        forecastData=getProcessedData(keyword, language, startDate, endDate, horizon)
        response=insertTrendData(userID,trendName,groupName,keyword,startDate,endDate,horizon,language,forecastData)
        return response'''
    
    try:
        videoLink=request.args.get('videoLink')
        return render_template("public/videos.html",videoLink_mp4='/static/videos/'+videoLink+'.mp4',videoLink_webm='/static/videos'+videoLink+'.webm')
    except Exception as error:
        return str(error)

