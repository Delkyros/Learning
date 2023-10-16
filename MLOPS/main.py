
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import requests
import pickle

#model
from sklearn.linear_model import LinearRegression

model = pickle.load(open('model.sav', 'rb'))
features =['tamanho', 'ano', 'garagem']

app = Flask(__name__)
#basic authentication
app.config['BASIC_AUTH_USERNAME'] = 'someone'
app.config['BASIC_AUTH_PASSWORD'] = 'password'

auth = BasicAuth(app)

@app.route('/')
def home():
    return 'My first API.'

@app.route('/sentiment/<phrase>')
@auth.required

def sentiment(phrase):
    tb = TextBlob(phrase)
    polarity = tb.sentiment.polarity
    return "Polarity: {}".format(polarity)

@app.route('/pricing/', methods=['POST'])
@auth.required
def pricing():
    data = request.get_json()
    input_data = [data[col] for col in features]
    price = f" A house with a size of {input_data[0]}, built in the year of {input_data[1]} and with {input_data[2]} garage size has the price of {model.predict([input_data])[0]:.2f}"
    return price

app.run(debug=True)