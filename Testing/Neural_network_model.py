
import pandas as pd
import tensorflow as tf

# first neural network with keras tutorial
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing


train_dataset =  pd.read_csv('https://github.com/SasikalaGV/MLProject2020/tree/main/data/powerproduction.csv',
names=["Speed","Power"])

dataset = train_dataset.head(20)
print (dataset)

print("test")

