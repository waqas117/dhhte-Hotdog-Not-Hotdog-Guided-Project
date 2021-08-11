# Pytorch  stuff 
import torchvision.transforms as transforms
import torch
import torch.nn as nn
import torchvision.models as models
# PIL library for images 
from PIL import Image

from flask import Flask,redirect,url_for, render_template, request,session
import os.path
import tempfile
import io
import os
import base64
import logging


dir_path = os.path.dirname(os.path.realpath(__file__))

app=Flask(__name__)


public=True


ABELS_ARRAY=2

LABELS_ARRAY=["HOTDOG","NOT HOTDOG"]


project_name="HOTDOG OR  NOT HOTDOG "
application_name="HOTDOG OR  NOT HOTDOG "

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(512, len(LABELS_ARRAY))
model.load_state_dict(torch.load(os.path.join(dir_path,"hotdog_detector.pt")))
model.eval()
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

my_transforms= transforms.Compose([transforms.Resize((224, 224))
                                ,transforms.ToTensor()
                                , transforms.Normalize(mean, std)])

@app.route("/")
def home():
    
    return render_template("index.html", flag=False,
        application_name=application_name, project_name=project_name)

@app.route('/', methods=['GET', 'POST'])
def upload():

    uploaded_file = request.files['files']

    predicted = ""
    img = ""
    if uploaded_file.filename != '':
        data = io.BytesIO(uploaded_file.read())
        image = Image.open(data).convert('RGB')
    
        tensor = my_transforms(image).unsqueeze(0)
        z=model(tensor)
        _,yhat=torch.max(z.data, 1)

        predicted = "Deep network prediction: " + LABELS_ARRAY[yhat]

        img = str(base64.b64encode(data.getvalue()))[2:-1]
    
    

    return render_template("index.html",image_class=predicted, img=img, flag=True,
        application_name=application_name, project_name=project_name)


PORT  = os.environ.get('PORT') or 8080
DEBUG = os.environ.get('DEBUG') != 'TRUE'

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)