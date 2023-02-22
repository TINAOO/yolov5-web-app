
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

- In `app.py`, [run detect.py](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=subprocess.run(%5B%27python3%27%2C%20%27detect.py%27%2C%20%27%2D%2Dsource%27%2C%20os.path.join(uploads_dir%2C%20secure_filename(video.filename))%2C%20%27%2D%2Dsave%2Dtxt%27%5D)) with prefered parameters for your need
```bash
subprocess.run(['python3', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename)), '--save-txt']) 
```

Details on text file row-counting implementation, go to [app.py](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=count%20%3D%200,.close()). Code block is pasted below for your reference.
- In this code block, `count` is the variable to track the number of rows in the text file. `count` is incrementing at [`count = count + 1`](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=count%20%3D%20count%20%2B%201%20%23%20counting%20rows%20in%20the%20text%20file%2C%20increment%20count%20as%20we%20go%20thru%20line)

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

- Row count is returned to `index.js` file, along with user's uploaded video name. [Code block is shown below.](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=obj%20%3D%20secure_filename,return%20data)
```bash
obj = secure_filename(video.filename) # video file name. For instance, street_vid.mp4
data = obj + ":" + str(count) # return file name and count of rows as data to ---> index.js file
return data
```

- In `index.js` file, we get data returned from [ `app.py`](https://github.com/TINAOO/yolov5-web-app/blob/main/app.py#:~:text=obj%20%3D%20secure_filename,return%20data). 

The data is [parsed](https://github.com/TINAOO/yolov5-web-app/blob/main/static/index.js#:~:text=vid_name%20%3D%20data,count%20from%20data) to get video name and row number. [As shown below.](https://github.com/TINAOO/yolov5-web-app/blob/main/static/index.js#:~:text=vid_name%20%3D%20data,count%20from%20data)
```bash
vid_name = data.split(":")[0] // parse vid name from data
num_rows = data.split(":")[1] // parse row count from data
```

Then, the row number is [passed](https://github.com/TINAOO/yolov5-web-app/blob/main/static/index.js#:~:text=%24(%22%23row%22).html(%22number%20of%20rows%3A%20%22%2Bnum_rows)%20//%20pass%20number%20of%20rows%20to%20%2D%2D%2D%3E%20index.html) to [`index.html`](https://github.com/TINAOO/yolov5-web-app/blob/main/templates/index.html) file to be rendered on the web page. Along with download link for processed video and result text file. All saved in `static` folder. [As shown below.](https://github.com/TINAOO/yolov5-web-app/blob/main/static/index.js#:~:text=%24(%22%23download,%2Bnum_rows))
```bash
$("#download").attr("href", "static/" + vid_name); // download link for processed video
$("#download-txt").attr("href", "static/" + vid_name.split(".")[0]+"_result.txt"); // download link for text result
$("#row").html("number of rows: "+num_rows) // pass number of rows to ---> index.html
```

- `index.html` render the UI components. [Code block is pasted below.](https://github.com/TINAOO/yolov5-web-app/blob/main/templates/index.html#:~:text=%3Cdiv%20id,%3C/span%3E)
```bash
<div id="link1">
  <a href="" id="download" download>Download video</a>
    </div>
      <div id="link2"> 
        <a href="" id="download-txt" download>Download text file</a>
      </div>
      <!-- get number of rows from index.js and render on webpage -->
      <span id="row"></span> 
```