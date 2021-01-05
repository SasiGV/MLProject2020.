import os

# Add flask for web app
from flask import Flask
import numpy as np

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


#from keras.models import load_model
model=keras.models.load_model("Model_NN.h5")

# Load Keras model from saved files "Model_NN.json" & "Model_NN.h5". Code adapted from
# https://machinelearningmastery.com/save-load-keras-deep-learning-models/
# load json and create model
#json_file = open('testmodel.json', 'r')
json_file = open('Model_NN.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = kr.models.model_from_json(loaded_model_json)


# load weights into new model
model.load_weights("Model_NN.h5")
#model=model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
#print("Compiled")
#print(model.summary())
#print("Loaded model from disk")
#model_S = load_model("Model_NN.h5")

# Copy of variables and function from Jupyter Notebook
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
      return round(model.predict([ws/Speed_F])[0][0]*Power_F, 3)
   else:
      #print("Error")
      return 0

# Tested the output for different I/Ps
#test = power_output(15)
#print(f"power output for wind speed 15 is: {test}")
#test = power_output(17)
#print(f"power output for wind speed 15 is: {test}")

#print("Input From screen")
#print(round(model.predict([wind/Speed_F])[0][0]*Power_F, 3))

app = Flask(__name__, static_url_path='', static_folder='static')



# Add root route.
@app.route('/')
def index():
   # return "hello"
   return app.send_static_file('index.html')

# Add power route.
# curl http://127.0.0.1:5000/api/power/5
@app.route('/api/power/<int:speed>')
def power(speed):
   #return {"power": str([[50]])}
   #p = model.predict([[speed]])
   p = 0
   p = power_output(speed)
   return {"power": p}
   
   
# Run in debug mode
if __name__ == "__main__":
   app.run(debug=True)