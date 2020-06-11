

import time
import pandas as pd
import os
import requests
import json
from PIL import Image
import urllib.request, urllib.parse, urllib.error
import numpy as np
import fileNamesAndAPI


#creating a start time object        
startTime = time.time()
#Extract the testData
testData = fileNamesAndAPI.testfile({Enter your url that will download the contains fileName and filePath})
#converting fileName to integer
testData[{fileName}] = testData[{fileName}].astype(int)

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

#creating a dataframe whcih will hold the logIn and verifiedID indicator
solutionData = pd.DataFrame(columns = ["loginID" ])
solutionData["loginID"] = testData["custID"]
solutionData.insert(1,"verifiedID",0)

#create a dataframe to hold train data
knownData=pd.read_csv({Enter your file that contains the training data})

#creating a list
samplefaceId = []

#Extract the faceId for test Database
for i in range(len(testData)):
    imageData = open(testData.loc[i,'filePath'],"rb").read()
    response=requests.post(detectEP,params=params,headers=headers,data = imageData)
    time.sleep(3.5)
    jsonobject = json.dumps(response.json()[0]['faceId'])
    jsonobject = jsonobject.replace('"','')
    samplefaceId.append(jsonobject)
    
#inserting faceIds  
testData['samplefaceId'] = samplefaceId

#create a dataframe by merge testdata and train data on fileName
combinedData = pd.merge(testData,knownData,how='inner',on='custID',suffixes=('_sample','_known'))

#Verifying for faces using faceId from detect and personId in persongroup person in persongroup
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
            #if confidence interval is greater than 70% then 1 will be inserted
            solutionData["verifiedID"][solutionData["loginID"]==combinedData.loc[j,"custID"]] = 1
        break
 
solutionData.to_csv("solutionFile.csv",index=False)
print(time.time() - startTime)
       
