from flask import session, jsonify
from functools import wraps
from flask import flash


def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        target_user_id = kwargs.get('user_id')

        # Ensure the logged-in user is the target user
        if str(user_id) != str(target_user_id):
            flash("You are not authorized to perform this action.", "warning")
            return jsonify({"error": "Unauthorized"}), 403

        return f(*args, **kwargs)
    return decorated_function
