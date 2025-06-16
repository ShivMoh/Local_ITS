import socket
import json
from typing import Dict
import os
from typing import Dict, List
import gc
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, stream_with_context, send_from_directory
)
# from werkzeug.security import check_password_hash, generate_password_hash, secure_filename
from markupsafe import escape

UPLOAD_FOLDER = '../storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

from flask_cors import CORS
# from flaskr.db import get_db
bp = Blueprint('file', __name__, url_prefix='/file')

CORS(bp)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    if 'file' not in request.files:
      return {
        "success" : False,
        "message" : "No files have been uploaded",
        "status" : 200
      }

    file = request.files['file']

    if file.filename == '':
      return {
        "success" : False,
        "message" : "No selected file",
        "status" : 200
      }
    if file and allowed_file(file.filename):
      filename = file.filename
      file.save(os.path.join(UPLOAD_FOLDER, filename))

      return {
        "success" : True,
        "message" : "File uploaded successfully",
        "status" : 200
      }

@bp.route('/pdfs/<filename>', methods=['GET'])
def serve_pdf(filename):
    return send_from_directory("/home/shivesh/Documents/python/its_solution/local_its/server/flaskr/storage/pdfs", filename)


