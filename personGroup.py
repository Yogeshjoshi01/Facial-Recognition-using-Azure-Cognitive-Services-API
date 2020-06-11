# -*- coding: utf-8 -*-
"""
Created on Fri May  8 17:18:12 2020

@author: yoges
"""

#FACE API Using person group
import time
import pandas as pd
import os
import requests
import json
from PIL import Image
import urllib.request, urllib.parse, urllib.error
import numpy as np
import genTestFile
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64

subscriptionKey = genTestFile.subscriptionKey()
EndPoint = genTestFile.pgEndPoint()
EndPoint1 = genTestFile.pgpEndPoint()
EndPoint2 = genTestFile.pgpAddEndPoint()
trainEndPoint = genTestFile.trainEndPoint()

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscriptionKey
}

#params = {'personGroupId':'yj610'}
body = {
    'name':'knownfaces',
    'recognitionModel': 'recognition_02'
}


#creating a person group
response = requests.put(url =EndPoint, headers=headers,json=body)
#response.status_code
print(response.url)


knownData = pd.read_csv("cleanedFile1.csv")
personId = []
for i in knownData.custID.unique():
    body1 = {
        'name':str(i)
        }
    response1 = requests.post(url =EndPoint1,headers =headers,json = body1)
    time.sleep(3.5)
    personId.append(response1.json()['personId'])
    
df = pd.DataFrame(columns=['personId'])
df['personId']=personId
df.to_csv('personId.csv',index=False)
#create person group person
#response1 = requests.post(url =EndPoint1,headers =headers,json = body1 )
#response1.status_code
#print(response1.text)
#print(response1.url)
#print(response1.json())
headers1 = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscriptionKey
}

df=pd.read_csv('personId.csv')
flag = 0
number = 0
for i in knownData.custID.unique():
    personID = df.loc[flag,'personId']
    EpUrl = 'https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1/persons/{}/persistedFaces'.format(personID)
    for j in knownData[knownData["custID"]==i].index:
        url = knownData.loc[j,'filePath']     
        imageData1 = open(url,"rb").read()
        response2 = requests.post(url = EpUrl,headers=headers1,data = imageData1)
        time.sleep(4)
        print(flag,number)
        number +=1
    flag+=1



#TRAIN PERSON GROUP
headers3 = {
    'Ocp-Apim-Subscription-Key': subscriptionKey
}

reponse3 = requests.post(url=trainEndPoint,headers =headers3)
response4 = requests.get(url = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1/training",headers=headers3)
response5 = requests.get(url = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1",headers=headers)
print(response4.status_code)
print(response4.text)   
#headers2 = { 'Ocp-Apim-Subscription-Key': subscriptionKey   }
#getEP = 'https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1/persons/558fd59a-aa8a-427f-ae2b-0e9f5c57dcf5'    
#response3 = requests.get(url =getEP,headers=headers2 )
#print(response3.text)
#response3.status_code