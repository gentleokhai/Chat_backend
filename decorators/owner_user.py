from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import flash


def owner_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        target_user_id = kwargs.get('user_id')

        # Ensure the logged-in user is the target user
        if str(current_user_id) != str(target_user_id):
            flash("You are not authorized to perform this action.", "warning")
            return jsonify({"error": "Unauthorized"}), 403

        return f(*args, **kwargs)
    return decorated_function
