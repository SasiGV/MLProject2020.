# Add flask for web app
from flask import Flask
import numpy as np
#import flask as f1
#from numpy import Numpy
#numpy for numerical work
#import numpy as np

#------------------------------------------
# Install numpy=1.19.3 to avoid issues while using python 3.9.1
#https://stackoverflow.com/questions/64654805/how-do-you-fix-runtimeerror-package-fails-to-pass-a-sanity-check-for-numpy-an
#------------------------------------------

# Silence tensorflowstartup warnings. Code adapted from
# https://stackoverflow.com/a/65215118
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import tensorflow.keras as kr

# Load Keras model from saved files "testmodel.json" & "my_model.h5". Code adapted from
# https://machinelearningmastery.com/save-load-keras-deep-learning-models/
# load json and create model
json_file = open('testmodel.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = kr.models.model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("testmodel.h5")
#print("Loaded model from disk")

# Copy of variables and function from Project.ipynb
# Set normalisation factors
wsF = 25
poF = 120
# Function to predict power output based on inputted wind speeds
def power_output(windspeeds):
   """ Function to predict power output based on inputted wind speeds
      Acceptable inputs include numbers or a list of numbers
   """
   # Set the cut off wind speeds
   minWS, maxWS = 3, 24.5

   # If wind speed is inside the cut off levels
   if windspeeds > minWS and windspeeds < maxWS:
      ws = np.array([windspeeds])
      return round(model.predict(ws/wsF)[0][0]*poF, 3)
   else:
      #print("Error")
      return 0

# Function test. Also initialise the function.
test = power_output(10)
# print(f"power output for wind speed 10 is: {test}")




# create a new web app
#app = f1.flask(__name__)

#Add root route#
#@app.route('/')
#def stdnor():
#    return {'Value': np.random.standard_normal()}

app = Flask(__name__, static_url_path='', static_folder='static')

# Add root route.
#@app.route('/')
#def index():
#   # return "hello"
#   return app.send_static_file('index.html')

# Add power route.
# curl http://127.0.0.1:5000/api/power/5
#@app.route('/api/power/<speed>')
#def power(speed):
#   s = float(speed)
#   # get power from power curve model
#   return {"power" : power_output(s)}
#def index():
#    return 'HELLO'

# Run in debug mode
#if __name__ == "__main__":
#   #app.run(debug=True)
#   app.run()


# Add root route.
@app.route('/')
def index():
   # return "hello"
   return app.send_static_file('index.html')

# Add power route.
# curl http://127.0.0.1:5000/api/power/5
@app.route('/api/power/<speed>')
def power(speed):
   s = float(speed)
   # get power from power curve model
   return {"power" : power_output(s)}

# Run in debug mode
if __name__ == "__main__":
   app.run(debug=True)