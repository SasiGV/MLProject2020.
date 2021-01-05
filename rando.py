import os

# Add flask for web app
from flask import Flask
import numpy as np
#import flask as f1
#from numpy import Numpy
#numpy for numerical work
#import numpy as np
import joblib

import tensorflow as tf
from tensorflow import keras

# For restoring a keras model.
from tensorflow.keras.models import load_model


#------------------------------------------
# Install numpy=1.19.3 to avoid issues while using python 3.9.1
#https://stackoverflow.com/questions/64654805/how-do-you-fix-runtimeerror-package-fails-to-pass-a-sanity-check-for-numpy-an
#------------------------------------------

# Silence tensorflowstartup warnings. Code adapted from
# https://stackoverflow.com/a/65215118
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import tensorflow.keras as kr
#from tensorflow.keras.models import Sequential 


# Import my SVM regression model and the scaler to apply to x before predict.
svmreg = joblib.load("svm-reg.pkl")
#print(svmreg.predict(scaler.transform([[t]])), "for t= ", t)


#from keras.models import load_model
model=keras.models.load_model("Model_NN.h5")

#model.save_weights()
# Load Keras model from saved files "Model_NN.json" & "Model_NN.h5". Code adapted from
# https://machinelearningmastery.com/save-load-keras-deep-learning-models/
# load json and create model
#json_file = open('testmodel.json', 'r')
json_file = open('Model_NN.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
#with open('Model_NN.json','r') as f:
 #   loaded_model_json = f.read()
model = kr.models.model_from_json(loaded_model_json)
#New_model_Json = model_from_json(loaded_model_json)

#Now load weights into new model
#New_model_Json.load_weights("Model_NN.h5")
#print("Loaded model from disk")

#modelJson = kr.models.model_from_json(loaded_model_json)

# load weights into new model
model.load_weights("Model_NN.h5")
#model=model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
print("Compiled")
print(model.summary())
#print("Loaded model from disk")
model_TEST = load_model("neural-nw.h5")
model_S = load_model("Model_NN.h5")

# Copy of variables and function from Project.ipynb
# Set normalisation factors
wsF = 25
poF = 120
Speed_F=25
Power_F=120
wind=20
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
      return round(model.predict([wind/Speed_F])[0][0]*Power_F, 3)
   else:
      #print("Error")
      return 0

# Function test. Also initialise the function.
#test = power_output(15)
# print(f"power output for wind speed 10 is: {test}")

print("Input From screen")
print(model.predict([wind/Speed_F])[0][0]*Power_F, 3)

app = Flask(__name__, static_url_path='', static_folder='static')



# Add root route.
@app.route('/')
def index():
   # return "hello"
   return app.send_static_file('index.html')


########## Tell flask to make model 2 available at /model2 ##########
# model 2 is support vector machine regression
# file: svm-reg.pkl
# scaler: scalerX.pkl
# How to get the data into this function? Via the url, goes with request.
@app.route('/api/model2/<int:w>')
# curl test at 127.0.0.1:5000/api/model2/5 ok   
def model2(w):
    # return {"value": w * w} # works with curl & on page

    # Make the prediction using our model.
    p = svmreg.predict(scaler.transform([[w]]))
    # print(p[0]) # test format of prediction.
    return {"value": str(p[0])} # Object must be a string.

# Add power route.
# curl http://127.0.0.1:5000/api/model/5
@app.route('/api/model/<int:w>')
def model(w):
    # return "Wind speed is " + str(w) # works with curl
    # return {"value": w * w} # works with curl & on page
    
    # Make the prediction using our model
    p = model_TEST.predict([[w]]) # TypeError: Object of type ndarray is not JSON serializable if try to return this
    # print(p) # test - [[99.785995]]
    # print(p[0][0]) # test - 99.785995 TypeError: Object of type float32 is not JSON serializable if try this
    return {"value": str(p[0][0])} # Object must be a string

# Add power route.
# curl http://127.0.0.1:5000/api/power/5
@app.route('/api/power/<int:w>')
def power(speed):
   ##s = float(speed)
   # get power from power curve model
   ##return {"power" : power_output(s)}
   #return {"power": str([[50]])}
   p = model_S.predict([[w]])
   return {"value": str(p[0][0])} #
   
   
# Run in debug mode
if __name__ == "__main__":
   app.run(debug=True)