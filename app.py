from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, send_file
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import shutil
import pandas as pd
import glob
import time
import numpy as np
import matplotlib.pyplot as plt
import warnings
import re

app = Flask(__name__)


uploads_dir = os.path.join(app.instance_path, 'uploads')
app_dir = os.path.dirname(app.instance_path)
os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def hello_world():
    return render_template('index.html')


def tracking(d, file_path):
    warnings.filterwarnings("ignore")
    tic = time.time()
    d['id']=-1 # default id
    n = 15  # the tails would be searched in next 5 frames to avoid loosing particle
    id = 0 #first id # increases with every new trail
    theta = 15 # +/- angle acceptable deflection of next position 
    fp = d.iloc[0] # first/lead particle assigned to varialble
    fid = d.index[0] # The index of firsst particle in database variable 'd'

    while (True):    #breaks when all the identified particles are given id (id != -1) 
        if(fp['id']==-1): # allots new id if id is -1 (unassigned)
            fp['id']=id
            id = id+1;
        temp = d[(d['# frame']>fp['# frame']) & (d['# frame']<=fp['# frame']+n) & (d['id']==-1)] #temp stores data of next n frames where trail is searched
        temp = temp[temp['xc']>fp['xc']]
        temp['theta'] = 200 # to store the angle theta between 2 positions wrt to horizontal axis
        temp['dis'] = 500   # distance between 2 positions 
        temp['theta'] = np.abs((180/np.pi)*np.arctan((temp['yc']-fp[['yc']].to_numpy())/(temp['xc']-fp[['xc']].to_numpy()))) #calculating theta
        temp['dis'] = np.sqrt((temp['yc']-fp[['yc']].to_numpy())**2+(temp['xc']-fp[['xc']].to_numpy())**2) # calculating distance   
        temp = temp[temp['theta']<theta] #filter to remove positions not within angular deviation  
        temp=temp.sort_values(by = ['# frame','theta','dis'], ascending = [True,True,True]) #sorting to select postion nearest frame
        d.at[fid,'id']=fp['id'] #updating the data base with id of lead particle 
        if(len(temp>0)): # checks if there are any trails ahead
            d.loc[temp.index[0],'id']=fp['id'] #updates data base with next position
            temp.iloc[0,-3]=fp['id'] #storing id to transfer it to next prediction
            fp = temp.iloc[0]
            fid = temp.index[0] 
            #print(temp)
        else:
            if(len(d[d['id']==-1])>0):
                fp = d[d['id']==-1].iloc[0]
                fid = d[d['id']==-1].index[0]
                #print('else')
            elif(len(d[d['id']==-1])==0):
                break
        #print(temp)
    toc = time.time()
    print("Time taken to process files=",-1*(tic-toc))

    # overwirte existed text file
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'a') as f:
        dfAsString = d.to_string(header=True, index=False)
        f.write(dfAsString)
    return len(d['id'].unique()) # return number of particles

@app.route("/detect", methods=['GET','POST'])
def detect():
    if not request.method in ['GET','POST']:
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    name = video.filename.split('.')[0]
    # parse video name
    while not name[0].isalnum(): name = name[1:] # video name must start with alphanumeric
    name = re.sub(r'\W+', '_', name) 
    while not name[-1].isalnum(): name = name[0:-1]
    labels_dir = os.path.join(app_dir, 'static', 'labels')
    if os.path.exists(labels_dir):
        shutil.rmtree(labels_dir)

    subprocess.run("ls")
    # run the detect.py file with parameters
    subprocess.run(['python3', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename)), '--save-txt']) 

    file_list = os.listdir(labels_dir) # get all label files
    result_dir = os.path.join(app_dir, 'static') # save combined result to this directory
    file_path = os.path.join(result_dir, name+'.txt') # combined text file path
    print("NAME file path  ",file_path)
    # overwrite existed text file
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path,'w') as file: 
        for f in file_list:
            if(name in f):
                substr1_split = f.split('.')[0].split('_')
                frame = substr1_split[len(substr1_split)-1] # last element of substr arry = frame number
                with open(os.path.join(labels_dir, f)) as input_file:
                    for line in input_file: # iterate each line in all label files
                        file.write(frame+' ') # write frame number  
                        file.write(line)
    file.close()

    # Column names to be added
    column_names=["# frame","class","xc","yc","x","y"]

    # Add column names while reading a text file
    df = pd.read_csv(file_path, sep=" ", names=column_names)
    df = df[["class","xc","yc","x","y","# frame"]]
    d = df
    d.reset_index(drop="index",inplace=True)
    d=d.sort_values(by = ['# frame'], ascending = [True]) 
    d['id'] = -1

    count = tracking(d, file_path) # get number of particles
    
    obj = secure_filename(video.filename) # video file name. For instance, cell_vid.mp4
    data = obj + ":" + str(count) # return file name and number of particles as data to ---> index.js file
    return data

@app.route("/retrieve/<file>", methods=['GET'])
def retrieve(file):
    print('RETRIEVEING file: ',file)
    result_dir = os.path.join(app_dir, 'static')
    file_path = os.path.join(result_dir, file)
    print('RETRIEVEING file path: ', file_path)
    return send_file(file_path)

@app.route("/opencam", methods=['GET'])
def opencam():
    print("here")
    subprocess.run(['python3', 'detect.py', '--source', '0'])
    return "done"
    
