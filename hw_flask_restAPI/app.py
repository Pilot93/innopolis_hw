#make simple server
from flask import Flask, jsonify, request
app = Flask(__name__)

#make tensor from picture

import torchvision.transforms as transforms
from PIL import Image

import io

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

#Create model

from torchvision import models

# убедитесь что `pretrained` = `True` :
model = models.densenet121(pretrained=True)
# Поскольку мы используем нашу модель только для вывода, переключитесь на режим `eval` :
model.eval()

#creating nice and readeble class name from json file

import json

# проверьте путь!
imagenet_class_index = json.load(open('./imagenet_class_index.json'))

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]

@app.route('/predict', methods=['POST']) 
def predict():
    if request.method == 'POST':
        # we will get the file from the request
        file = request.files['file']
        # convert that to bytes
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
    return jsonify({'class_id': class_id, 'class_name': class_name})
