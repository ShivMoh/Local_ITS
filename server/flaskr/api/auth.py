import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/hello', methods=['GET', 'POST'])
def hello_world() -> str:
    return "*in robot voice* HeLlo WoRlD"
