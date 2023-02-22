
## <div align="center">YOLOv5 Web Application</div>

## Steps to install, set up environment, and run code

Clone repo and install [requirements.txt](https://github.com/TINAOO/yolov5-web-app/blob/main/requirements.txt) 


```bash
git clone https://github.com/TINAOO/yolov5-web-app.git # clone
cd yolov5-web-app
pip install --upgrade pip  # upgrade pip if necessary
pip3 install -r requirements.txt  # install
```
Create an environment for flask
```bash
python3 -m venv venv
```
Activate the environment
```bash
. venv/bin/activate
```
Within the activated environment, use the following command to install Flask:
```bash
pip3 install Flask
```

Start run the project
```bash
flask run
```

Upload video by choosing the mp4 file. Then visit http://127.0.0.1:5000/ in your browser. 

Processed video and text file are saved in the `static` directory

<p align="center">
<img src="https://github.com/TINAOO/yolov5-web-app/blob/main/1.png" width="450">
</p>

<p align="center">
<img src="https://github.com/TINAOO/yolov5-web-app/blob/main/2.png" width="450">
</p>

<p align="center">
<img src="https://github.com/TINAOO/yolov5-web-app/blob/main/3.png" width="450">
</p>


## Implementation details
If you need to make changes on the parameters to run detect.py, go to [app.py](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py)

- In app.py, [run detect.py](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=subprocess.run(%5B%27python3%27%2C%20%27detect.py%27%2C%20%27%2D%2Dsource%27%2C%20os.path.join(uploads_dir%2C%20secure_filename(video.filename))%2C%20%27%2D%2Dsave%2Dtxt%27%5D)) and update it with prefered parameters for your need

Details on text file row-counting implementation, go to [app.py](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=count%20%3D%200,.close()). Code block is pasted below for youre reference.
- In this code block, `count` is the variable to track number of rows in the text file. `count` is incrementing at [`count = count + 1`](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=count%20%3D%20count%20%2B%201%20%23%20counting%20rows%20in%20the%20text%20file%2C%20increment%20count%20as%20we%20go%20thru%20line)

```bash
count = 0 # initialize a variable to count rows in the file
    with open(file_path,'w') as file: 
        for f in file_list:
            if(name in f):
                substr1_split = f.split('.')[0].split('_')
                frame = substr1_split[len(substr1_split)-1] # last element of substr arry = frame number
                with open(os.path.join(labels_dir, f)) as input_file:
                    for line in input_file: # iterate each line in all label files
                        count = count + 1 # counting rows in the text file, increment count as we go thru line
                        file.write(frame+' ') # write frame number  
                        file.write(line)
    file.close()
```

- Row count is returned to `index.js` file, along with user's uploaded video name. [Code block as shown below.](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=obj%20%3D%20secure_filename,return%20data)
```bash
obj = secure_filename(video.filename) # video file name. For instance, street_vid.mp4
data = obj + ":" + str(count) # return file name and count of rows as data to ---> index.js file
return data
```

- In `index.js` file, we get data returned from [ `app.py`](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=obj%20%3D%20secure_filename,return%20data). The data is parsed to get video name and row number. [Code block as shown below.](https://github.com/TINAOO/yolov5-web-app/blob/main/static/index.js#:~:text=%24(%22%23download,to%20%2D%2D%2D%3E%20index.html) Then, the row number is passed to [`index.html`](https://github.com/TINAOO/yolov5-web-app/blob/main/templates/index.html) file to render the number of rows on the web page.
```bash
$("#download").attr("href", "static/" + vid_name); // download link for processed video
$("#download-txt").attr("href", "static/" + vid_name.split(".")[0]+"_result.txt"); // download link for text result
$("#row").html("number of rows: "+num_rows) // pass number of rows to ---> index.html
```


