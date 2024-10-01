from functools import wraps
from flask import session, jsonify
from models.user_model import User


def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        user = User.objects(pk=user_id).first()
        print("User ID from session:", user_id)
        print("User from database:", user)
        if not user or not user.is_superuser:
            return jsonify({
                "error": "You must be a superuser to access this page."
                }), 403
        return f(*args, **kwargs)
    return decorated_function
