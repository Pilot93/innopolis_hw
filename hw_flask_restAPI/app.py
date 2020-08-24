#make simple server
from flask import Flask, jsonify, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_karl'

threshold = 10

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
    kek, y_hat = outputs.max(1)
    kekes = kek.detach().numpy()[0]
    predicted_idx = str(y_hat.item())
    arr_pred = imagenet_class_index[predicted_idx]
    return [arr_pred[0], arr_pred[1], kekes]

#check extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#upload file

@app.route('/upload', methods=['GET'])
def upload_file():
    return render_template('upload.html')

@app.route('/predict', methods=['POST']) 
def predict():
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part\n'
        # we will get the file from the request
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file\n'
        # convert that to bytes
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_bytes = file.read()
            class_id, class_name, foobar = get_prediction(image_bytes=img_bytes)
            if foobar < threshold:
                return jsonify({'class_id': class_id, 'class_name': class_name, 'probability': str(foobar), 'error' : 'Answer is not certain'})
        else:
            #print('Not a jpg')
            return 'Not a jpg image\n'
    return jsonify({'class_id': class_id, 'class_name': class_name, 'probability': str(foobar)})
