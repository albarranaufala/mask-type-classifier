"""
    Referensi:
    - https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html
    - https://github.com/avinassh/pytorch-flask-api
"""

import io
import json

import torch as pt
import torchvision.transforms as transforms

from PIL import Image

from flask import Flask, jsonify, request
from flask_cors import CORS

class_index = {
    0: "KAIN",
    1: "MEDIS",
    2: "SCUBA"
}
model = pt.load("MaskTypeClassifier_90_87.pth", map_location=pt.device("cpu"))
model.eval()


def transform_image(image_bytes):
    test_transform = transforms.Compose([
        transforms.Resize(256),          
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return test_transform(image)


def get_prediction(image_bytes):
    tensor_img = transform_image(image_bytes=image_bytes)
    outputs = model(tensor_img.unsqueeze(0))
    predicted_idx = outputs.max(1).indices

    return class_index[predicted_idx.item()]


app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_name = get_prediction(image_bytes=img_bytes)
        return jsonify({'class_name': class_name})


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'hello':'test success'})

app

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
