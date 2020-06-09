# -*- coding: utf-8 -*-
"""
Created on Thu May  7 17:01:19 2020

"""

import pandas as pd
import requests
from zipfile import ZipFile
import re
import os
import shutil

#Function used to clean and extract the FileNames/testData from DropBox Url
#This will not be needed for people who already have testData
def testfile(link):
    #Pass the dropBox link
    url1 = link
    
    #Pass a get request to create an object
    testData = requests.get(url1)
    
    #Create a .zip object in the directory
    with open('testData.zip','wb') as data: 
        data.write(testData.content)
    
    #Make a directory that contains only testData
    os.mkdir("testCustID")
        
    #Extracting contents of .zip file    
    with ZipFile("testData.zip","r") as zipObj:
        zipObj.extractall("testCustID")
        
    #removing .zip file
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
    #Access key to pass request calls to Azure
    subscriptionKey = "{Enter your subscription key}"
    return subscriptionKey

def detectEndPoint():
    #EndPoint Url for detecting the face
    faceApiUrl = "https://{Enter your endpoint URL}/face/v1.0/detect"
    return faceApiUrl

def verifyEndPoint():
    #EndPoint Url for verifying the face
    faceApiUrl1 = "https://{Enter your endpoint URL}/face/v1.0/verify"
    return faceApiUrl1
    
def pgEndPoint():
    #Creates a PersonGroup(Parent Folder)
    faceApiUrl2 = "https://{Enter your endpoint URL}/face/v1.0/persongroups/{personGroupId}"
    return faceApiUrl2

def pgpEndPoint():
    #Creates a PersonGroup Person which can thought as a subfolder inside a parent folder(PersonGroup)
    faceApiUrl3 = "https://{Enter your endpoint URL}/face/v1.0/persongroups/{personGroupId}/persons"
    return faceApiUrl3

def pgpAddEndPoint():
    #Adds the faces inside PersonGroup Person(subfolder)
    faceApiUrl4 = "https://{Enter your endpoint URL}/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces"
    return faceApiUrl4

def trainEndPoint():
    #Trains the PersonGroup
    faceApiUrl5 = "https://{Enter your endpoint URL}/face/v1.0/persongroups/{personGroupId}/train"
    return faceApiUrl5
