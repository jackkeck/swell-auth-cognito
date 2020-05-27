from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, escape, redirect, request, jsonify
from flask_awscognito import AWSCognitoAuthentication

flask_app = Flask(__name__)
aws_auth = AWSCognitoAuthentication(flask_app)

@flask_app.route('/')
@aws_auth.authentication_required
def index():
    claims = aws_auth.claims # also available through g.cognito_claims
    return jsonify({'claims': claims})

@flask_app.route('/aws_cognito_redirect')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    return jsonify({'access_token': access_token})

@flask_app.route('/login')
def login():
    login_url = flask_app.config['AWS_COGNITO_DOMAIN']+'/login?response_type=code&client_id='+flask_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']+'&redirect_uri='+flask_app.config['AWS_COGNITO_REDIRECT_URL']
    print  (jsonify({'sign_in_url': login_url}))
    return redirect(login_url)

@flask_app.route('/logout')
def logout():
    login_url = flask_app.config['AWS_COGNITO_DOMAIN']+'/login?response_type=code&client_id='+flask_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']+'&redirect_uri='+flask_app.config['AWS_COGNITO_REDIRECT_URL']
    return redirect(login_url)

app = FastAPI()
@app.get("/fast/")
def read_main():
    return {"message": "HOLDER FOR FAST ENDPOINTS"}

app.mount("/v1", WSGIMiddleware(flask_app))
