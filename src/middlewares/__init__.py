from flask import request, Response, json
from functools import wraps
import jwt
import os

def authentication_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        # Check if the Authorization header is present
        if 'Authorization' in request.headers:
            bearer_token = request.headers['Authorization']
            token = bearer_token.split(" ")[1]

        # If no token is provided, return an error
        if not token:
            return Response(
                        response=json.dumps({ "message": "A valid token is missing"}),
                        status=401,
                        mimetype='application/json'
                    )

        try:
            # Decode the token
            print(token)
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            # Check if the user is authorized
            # if data['username'] not in authorized_users or authorized_users[data['username']] != data['password']:
            #     return jsonify({'message': 'Token is invalid'}), 401

        except:
            return Response(
                        response=json.dumps({ "message": "Token is invalid"}),
                        status=401,
                        mimetype='application/json'
                    )

        # If the token is valid, call the decorated function
        return func(*args, **kwargs)

    return decorated