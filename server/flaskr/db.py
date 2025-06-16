import sqlite3
from datetime import datetime
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        print(current_app.config['DATABASE'])
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # remember that current app is like a special keyword. dw about it too much
    with current_app.open_resource('schema.sql') as f:
        print("database is databasing")
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command() -> None:
    init_db()
    click.echo("**In robot voice** Database initialized")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

sqlite3.register_adapter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
