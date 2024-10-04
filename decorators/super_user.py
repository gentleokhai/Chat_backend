from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.user_model import User


def superuser_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.objects(pk=current_user_id).first()
        if not user or not user.is_superuser:
            return jsonify({
                "error": "You must be a superuser to access this page."
                }), 403
        return f(*args, **kwargs)
    return decorated_function