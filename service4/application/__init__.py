from flask import Flask
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app=Flask(__name__)
app.config['SECRET_KEY'] = 'yes'

#___________________________________________________________x-ray configuration_____________________________________________

xray_recorder.configure(service='myapp')
XRayMiddleware(app, xray_recorder)

#_______________________________________code for app.config will go here for the environment__________________________________

from application import routes
