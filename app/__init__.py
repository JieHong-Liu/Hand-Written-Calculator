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


if __name__ == '__main__':
    # host 0.0.0.0 will auto connect
    app.run(host='0.0.0.0', port=3000, debug=False)
