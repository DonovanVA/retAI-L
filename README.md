# retail shoe product finder
This is a retail shoe product finder incorporating he use of YOLOV5 trained model on Roboflow

### 1. Install the dependencies
```
pip install -r requirements.txt
```

### 2. Set up environment variable

You will have to add a .env for global env variable ROBOFLOW_API_KEY
checkout :
https://blog.roboflow.com/launch-version-export-and-train-models-in-the-roboflow-python-package/
for more info

### 3. run python script

```
python main.py
```

### 4. Deploy to AWS EC2
You can configure amazon ec2 instance, I used c1.medium instance type and deep learning OS (Ubuntu ver 20)




