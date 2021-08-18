# -*- coding: UTF-8 -*-
import os
import numpy as np
import cv2
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from app import app
from wolfram import evaluation
from yolov3.yolo_detection_images import *

# route to open the index.html


@app.route('/home')
def upload_home():
    return render_template("index.html")


@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    question = request.values.get('question')  # pass js text to backend
    print(question)
    return evaluation(question)


@app.route('/test_predict', methods=['GET', 'POST'])
def yolo_predictions():
    try:
        img = request.files.get('')
        if(allowDataFormat(img)):
            img.save('image/'+img.filename)
            image = cv2.imread("image/"+img.filename)
            image_path = "image/"+img.filename
            yolov3_detection(image_path)
            height, width, channels = image.shape
            file_name = img.filename
            time.sleep(1)
            total_str = ''
            with open(image_path.split('.')[0]+'.txt', 'r') as f:
                total_str = f.read()
            os.remove("image/"+file_name)
            os.remove(image_path.split('.')[0]+'.txt')
            return 'The image you uploaded is '+file_name+'\n'+"and the image shape is " + str(height) + " * " + str(width)+'\nThe text is ' + total_str
        else:
            return ('The file you uploaded is not available.')
    except:
        return 'upload failed'

def allowDataFormat(image):
    # restrict the upload file.
    ok_list = ['jpg', 'jpeg', 'png', 'PNG', 'JPEG', 'JPG']
    file_name = image.filename.split('.')
    if(file_name[-1] in ok_list):
        return True
    else:
        return False


if __name__ == '__main__':
    # host 0.0.0.0 will auto connect
    app.run(host='0.0.0.0', port=80, debug=False)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3000, debug=False)
