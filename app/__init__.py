# -*- coding: UTF-8 -*-
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
CORS(app)

# route to open the index.html


@app.route('/')
def index():
    return 'Welcome to the HWC, make math easier~\nAdd /home after the link to upload ~~~'


# @app.route('/upload', methods=['POST', 'GET'])  # The default method is GET.
# def predict():
#     try:
#         img = request.files.get('')
#         if(allowDataFormat(img)):
#             img.save('image/'+img.filename)
#             image = cv2.imread("image/"+img.filename)
#             height, width, channels = image.shape
#             file_name = img.filename
#             os.remove("image/"+file_name)
#             return ('The image you uploaded is '+file_name+'\n'+"and the image shape is " + str(height) + " * " + str(width))
#         else:
#             return ('The file you uploaded is not available.')
#     except:
#         return 'upload failed'


# def allowDataFormat(image):
#     # restrict the upload file.
#     ok_list = ['jpg', 'jpeg', 'png', 'PNG', 'JPEG', 'JPG']
#     file_name = image.filename.split('.')
#     if(file_name[-1] in ok_list):
#         return True
#     else:
#         return False

if __name__ == '__main__':
    # host 0.0.0.0 will auto connect
    app.run(host='0.0.0.0', port=3000, debug=False)
