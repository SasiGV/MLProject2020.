# Add flask for web app
from flask import Flask

#import flask as f1
#from numpy import Numpy
#numpy for numerical work
#import numpy as np

# create a new web app
#app = f1.flask(__name__)

#Add root route#
#@app.route('/')
#def stdnor():
#    return {'Value': np.random.standard_normal()}

app = Flask(__name__)

app.route('/')
#app.route('/stdnor')
def stdnor():
    #return {'Value': np.random.standard_normal()}
    return 'Hello'