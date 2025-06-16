from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import json

from flask_cors import CORS

bp = Blueprint('test', __name__, url_prefix='/test')

CORS(bp)

@bp.route('/hello', methods=['GET', 'POST'])
def hello_world() -> str:
    return {
        "response" : "*in robot voice* HeLlo WoRlD",
    }

