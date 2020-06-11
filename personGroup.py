

#Setting up PersonGroup API 
import time
import pandas as pd
import os
import requests
import json
from PIL import Image
import urllib.request, urllib.parse, urllib.error
import numpy as np
#module that is created separately
import fileNamesAndAPI
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64

subscriptionKey = fileNamesAndAPI.subscriptionKey()
EndPoint = fileNamesAndAPI.pgEndPoint()
EndPoint1 = fileNamesAndAPI.pgpEndPoint()
EndPoint2 = fileNamesAndAPI.pgpAddEndPoint()
trainEndPoint = fileNamesAndAPI.trainEndPoint()

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscriptionKey
}

body = {
    'name':'knownfaces',
    'recognitionModel': 'recognition_02'
}


#1) CREATING PERSONGROUP
response = requests.put(url =EndPoint, headers=headers,json=body)
response.status_code

#importing the csv
knownData = pd.read_csv("Enter the csv which contains Known Faces")
#list that keeps track of individual persons
personId = []
#2) CREATING PERSONGROUP PERSON
for i in knownData.{fileName}.unique():
    body1 = {
        'name':str(i)
        }
    response1 = requests.post(url =EndPoint1,headers =headers,json = body1)
    #No more than 20 calls per minute
    time.sleep(3.5)
    #extracts the personId that will be passed later
    personId.append(response1.json()['personId'])
    
df = pd.DataFrame(columns=['personId'])
df['personId']=personId
#exporting the list of personId in directory
df.to_csv('personId.csv',index=False)

#3) ADDING FACES TO PERSONGROUP PERSON(SUBFOLDER) 
headers1 = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscriptionKey
}

df=pd.read_csv('personId.csv')
flag = 0
number = 0
for i in knownData.{fileName}.unique():
    personID = df.loc[flag,'personId']
    EpUrl = 'https://{Enter your endpoint url here}/face/v1.0/persongroups/{personGroupId}/persons/{}/persistedFaces'.format(personID)
    for j in knownData[knownData["custID"]==i].index:
        url = knownData.loc[j,'filePath']
        #read the image in bytes
        imageData1 = open(url,"rb").read()
        #Adding faces in each subfolder
        response2 = requests.post(url = EpUrl,headers=headers1,data = imageData1)
        time.sleep(4)
        print(flag,number)
        number +=1
    flag+=1

#4)TRAIN PERSON GROUP
headers3 = {
    'Ocp-Apim-Subscription-Key': subscriptionKey
}

reponse3 = requests.post(url=trainEndPoint,headers =headers3)
