
## <div align="center">YOLOv5 Web Application</div>

### Install and set up environment

Clone repo and install [requirements.txt](https://github.com/TINAOO/yolov5-web-app/blob/main/requirements.txt) 

```bash
git clone https://github.com/TINAOO/yolov5-web-app.git # clone
cd yolov5-web-app
pip install -r requirements.txt  # install
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
pip install Flask
```

Start run the project
```bash
flask run
```
Then visit http://localhost:5000/ in your browser. Processed video and text file are saved in the `static` directory