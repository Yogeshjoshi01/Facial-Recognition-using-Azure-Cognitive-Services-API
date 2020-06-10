In this repository there are two .py files. A detailed documentation is as follows:

fileNamesAndAPI.py - This file contains different funnction which will be imported in the parent file when runnning the script
1) testfile(link) - This funciton cleans the data and extract the fileNames and the filePath of your local computer where the image is saved
2) subscriptionKey() - an object will be returned that holds the key to Azure resource. This key can be found whille setting up the resource in Azure
3) detectEndPoint() - returns a url that will further be passed as a POST request to generate a faceId 
4) verifyEndPoint() - returns a url that will further be passed as a POST request to verify two faceId at a time
5) pgEndPoint() - returns a url that will further be passed as a PUT request to crate a Person Group.The reason to cude Person Group is that there can be a maximum of 30,000 requests calls under Azure Free Tier subscription and atmost 20 calls per minute. This slows down the process significantly. Hence, Azure provides Person Group API that can be imagined as a parent holder that will hold all the images. Under this parent folder subgroups of different images needs to be created using PersonGroup Person. Once it is created faces are to be added in each subfolder which will be eventually trained.
6) pgpEndPoint()- returns a url that will further be passed as a POST request to create a subfolder under Perosn Group
7) pgpAddEndPoint()- returns a url that will further be passed as a POST request to add faces in each subfolder
8) trainEndPoint() - returns a url that will further be passed as a POST request to train the data
