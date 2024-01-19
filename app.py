from flask import Flask, request,render_template, json
import joblib
import pandas as pd
import pickle
import tensorflow as tf
from werkzeug.utils import secure_filename
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import os

app = Flask(__name__)

@app.route('/',methods=["Get","POST"])
def index():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        
        filename = secure_filename(uploaded_file.filename)
        temp_path = 'temp_image.jpg'
        uploaded_file.save(temp_path)

    # Read the contents of the temporary file
        with open(temp_path, 'rb') as temp_file:
            file_contents = temp_file.read()
        
        # df = pd.read_csv(uploaded_file)
        # img = tf.io.read_file(uploaded_file)
        img = tf.io.decode_jpeg(file_contents, channels = 3)

        if img.shape[1] > img.shape[0]:
            img = tf.image.resize(img, size = (412, 548), antialias = True)
        if img.shape[1] < img.shape[0]:
            img = tf.image.resize(img, size = (412, 548), antialias = True)

        img = img / 255.0
        img = tf.expand_dims(img, axis = 0)  
        with open("model_test.pkl", 'rb') as file:
                network = joblib.load(file)
        predictions_test = network.predict(img)
        
        image = Image.fromarray((predictions_test[0] * 255).astype(np.uint8))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        temp_path = 'static/pics/result_image.jpg'
        if os.path.exists(temp_path):
            os.remove(temp_path)
        image.save(temp_path)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir,'static/result_image.jpg')
    # Encode the image as base64
        resultimagefolder = os.path.join('static', 'pics')
        app.config['UPLOAD']=resultimagefolder
        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return os.path.join(app.config['UPLOAD'], 'result_image.jpg')
        # return render_template('index.html', base64_image=base64_image)

if __name__ == '__main__':
     app.run(debug=True, port=5002)

