from flask import (Blueprint, request, url_for, abort)

bp = Blueprint('waifu', __name__, url_prefix='/api/waifu')

@bp.post('/chats')
def chats():
    try:
        payload = request.get_json()
        return payload
    
    except BaseException as err:
        return abort(400, err)