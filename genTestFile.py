# -*- coding: utf-8 -*-
"""
Created on Thu May  7 17:01:19 2020

@author: yoges
"""

import pandas as pd
import requests
from zipfile import ZipFile
import re
import os
import shutil

def testfile(link):
    url1 = link
    testData = requests.get(url1)
    
    with open('testData.zip','wb') as data: 
        data.write(testData.content)
    
    os.mkdir("testCustID")
        
    with ZipFile("testData.zip","r") as zipObj:
        zipObj.extractall("testCustID")
        
    os.remove("testData.zip")
        
    #Access filenames and filepath  for testdata inside the directory
    fileName = []
    filePath = []
    for names in os.listdir("testCustID"):
        fileName.append(names)
        filePath.append(os.path.join("testCustID",names))
        
    #Cleaning the filenames for Test data to extract 1st four characters
    cleanedFileName = []
    for i in range(len(fileName)):
        cleanedFileName.append(fileName[i].split(".",maxsplit=1)[0])
        
    testData = pd.DataFrame(columns = ["custID","filePath"])
    testData["custID"]=cleanedFileName
    testData["filePath"] = filePath
    
    return testData

def subscriptionKey():
    subscriptionKey = "73db40a0e0854b08b37f55c8e0043b6d"
    return subscriptionKey

def detectEndPoint():
    faceApiUrl = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/detect"
    return faceApiUrl

def verifyEndPoint():
    faceApiUrl1 = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/verify"
    return faceApiUrl1
    
def pgEndPoint():
    faceApiUrl2 = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1"
    return faceApiUrl2

def pgpEndPoint():
    faceApiUrl3 = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1/persons"
    return faceApiUrl3

def pgpAddEndPoint():
    faceApiUrl4 = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1/persons/{personId}/persistedFaces"
    return faceApiUrl4

def trainEndPoint():
    faceApiUrl5 = "https://demofaceapi610.cognitiveservices.azure.com/face/v1.0/persongroups/verifiedcustomerpics1/train"
    return faceApiUrl5