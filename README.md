
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
<img src="" width="450">
</p>

<p align="center">
<img src="" width="450">
</p>


