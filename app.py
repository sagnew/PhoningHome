from random import choice

from flask import Flask, request
from twilio import twiml
import requests

rover_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'

app = Flask(__name__)


@app.route('/sms', methods=['GET', 'POST'])
def get_mars_img():
    response = twiml.Response()
    sol = request.form['Body']
    request_params = {'api_key': 'DEMO_KEY', 'sol': sol}

    mars_data = requests.get(rover_url, params=request_params).json()
    photos = mars_data['photos']
    random_photo_url = choice(photos)['img_src']

    with response.message("Here's a picture from the Mars Rover :)") as m:
        m.media(random_photo_url)

    return str(response)

app.run(debug=True)
