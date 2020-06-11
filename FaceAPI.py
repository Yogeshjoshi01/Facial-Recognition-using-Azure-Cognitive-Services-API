# -*- coding: utf-8 -*-
"""
Created on Thu May  7 21:41:59 2020

@author: yoges
"""


import time
import pandas as pd
import os
import requests
import json
from PIL import Image
import urllib.request, urllib.parse, urllib.error
import numpy as np
import genTestFile


#creating a start time object        
startTime = time.time()
#Extract the testData
testData = genTestFile.testfile("https://www.dropbox.com/s/okqsr5e5fwrer0f/5124276.zip?dl=1")
testData["custID"] = testData["custID"].astype(int)

#extract subscription key, detect endpoint and verify endpoint
subscriptionKey = genTestFile.subscriptionKey()
detectEP = genTestFile.detectEndPoint()
verifyEP = genTestFile.verifyEndPoint()

#passing headers for detect
headers = {'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscriptionKey}

#passing parameters for detect
params = {'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    'recognitionModel':'recognition_02'}

#passing headers for verify
headers1 = {'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscriptionKey}

#creatinf a dataframe whcih will hold the logIn and verifiedID indicator
solutionData = pd.DataFrame(columns = ["loginID" ])
solutionData["loginID"] = testData["custID"]
solutionData.insert(1,"verifiedID",0)


knownData=pd.read_csv("cleanedFile2.csv")
#Combining sampledata and knowndata 



#creating a list
samplefaceId = []

#Extract the faceId for sample Database
for i in range(len(testData)):
    #imageUrl = (testData.loc[i,'filePath'])
    imageData = open(testData.loc[i,'filePath'],"rb").read()
    #print(imageData)
    response=requests.post(detectEP,params=params,headers=headers,data = imageData)
    time.sleep(3.5)
    jsonobject = json.dumps(response.json()[0]['faceId'])
    jsonobject = jsonobject.replace('"','')
    samplefaceId.append(jsonobject)
    
#inserting faceIds  
testData['samplefaceId'] = samplefaceId

combinedData = pd.merge(testData,knownData,how='inner',on='custID',suffixes=('_sample','_known'))


for i in combinedData['custID'].unique():
    for j in combinedData['custID'][combinedData['custID']==i].index:
        body = {"faceId":combinedData.loc[j,"samplefaceId"],
                "personGroupId":"verifiedcustomerpics1",
                "personId":combinedData.loc[j,"personID"]}
        response=requests.post(verifyEP,headers=headers1,json = body)
        time.sleep(3.5)
        confidence = float(json.dumps(response.json()['confidence']))
        print(confidence)
        if confidence > .7:
            solutionData["verifiedID"][solutionData["loginID"]==combinedData.loc[j,"custID"]] = 1
        break
 
solutionData.to_csv("5124276.csv",index=False)
print(time.time() - startTime)
       
#print(response.text)
##creating a list which will hold the knowndata faceID when calling azure detect API
#knownfaceId = []
#
##flag is needed to iterate through solution dataframe
#flag = 0
#
##Calling detect API and then verfiy API at the same time with a time sleep of 3.5 seconds in between
#for i in combinedData["custID"].unique():
#    for j in combinedData["custID"][combinedData["custID"]==i].index:
#        imageData1 = open(combinedData.loc[j,'filePath_known'],"rb").read()
#        response1 = requests.post(detectEP,params=params,headers=headers,data = imageData1)#(TOO MANY REQUESTS)
#        time.sleep(3.5)
#        jsonobject1 = json.dumps(response1.json()[0]['faceId'])
#        jsonobject1 = jsonobject1.replace('"','')
#        knownfaceId.append(jsonobject1)
#        body = {"faceId1":combinedData.loc[j,'samplefaceId'],
#                "faceId2":knownfaceId[flag],
#                "recognitionModel": "recognition_02"}
#        flag +=1
#        response2 = requests.post(verifyEP,json=body,headers=headers1)
#        time.sleep(3.5)
#        confidence = float(json.dumps(response2.json()['confidence']))
#        if confidence > .7:
#            solutionData["verifiedID"][solutionData["loginID"]==combinedData.loc[j,"custID"]] = 1
#            break
#        
#    
#        
#   
#print(time.time() - startTime)
#
##Calling PERSON ID
#solutionData = pd.DataFrame(columns = ["loginID" ])
#solutionData["loginID"] = testData["custID"]
#solutionData.insert(1,"verifiedID",0)
#
##creating a list
#samplefaceId = []
#
##Extract the faceId for sample Database
#for i in range(len(testData)):
#    #imageUrl = (testData.loc[i,'filePath'])
#    imageData = open(testData.loc[i,'filePath'],"rb").read()
#    #print(imageData)
#    response=requests.post(detectEP,params=params,headers=headers,data = imageData)
#    time.sleep(3.5)
#    jsonobject = json.dumps(response.json()[0]['faceId'])
#    jsonobject = jsonobject.replace('"','')
#    samplefaceId.append(jsonobject)
#
##inserting faceIds  
#testData['samplefaceId'] = samplefaceId
#
##import known Data
#knownData = pd.read_csv("cleanedFile1.csv")
#
##Combining sampledata and knowndata 
#combinedData = pd.merge(testData,knownData,how='inner',on='custID',suffixes=('_sample','_known'))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

#exporting the wolution File
