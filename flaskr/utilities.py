from .db import get_db
from flask import abort, g

devices_sql = 'SELECT * FROM {} WHERE private_device = 0'
empty_env_sql = 'SELECT * FROM {} WHERE private_device is NULL'
empty_sql = 'SELECT * FROM {} WHERE {} is NULL'

def get_env(id, check_user=True):
    env = get_db().execute(
        'SELECT p.id, env_name, created, user_id'
        ' FROM env p JOIN user u ON p.user_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if env is None:
        abort(404, "env id {0} doesn't exist.".format(id))
    if check_user and env['user_id'] != g.user['id']:
        abort(403)

    return env


def devices(sql):
    devices = get_db().execute(sql).fetchall()

    return devices 

def get_empty_vaule(sql):
    devices = get_db().execute(sql).fetchall()

    return devices