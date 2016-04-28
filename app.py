from random import choice
import os

from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient
import requests
import soundcloud

sounds_url = 'https://api.nasa.gov/planetary/sounds'
rover_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'

default_image = 'http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/ncam/NLB_486264973EDR_S0481570NCAM00546M_.JPG'

soundcloud_client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])
twilio_client = TwilioRestClient()

app = Flask(__name__)


@app.route('/call', methods=['POST'])
def play_space_sounds():
    request_params = {'api_key': 'DEMO_KEY', 'limit': 64}

    space_sounds_data = requests.get(sounds_url, params=request_params).json()
    space_sounds = space_sounds_data['results']
    track_url = choice(space_sounds)['stream_url']
    stream_url = soundcloud_client.get(track_url, allow_redirects=False)

    response = twiml.Response()
    response.play(stream_url.location)
    return str(response)


@app.route('/sms', methods=['GET', 'POST'])
def get_mars_img():
    response = twiml.Response()
    sol = request.form['Body']
    request_params = {'api_key': 'DEMO_KEY', 'sol': sol}

    try:
        mars_data = requests.get(rover_url, params=request_params).json()
        photos = mars_data['photos']
        random_photo_url = choice(photos)['img_src']

        with response.message("Here's a picture from the Mars Rover :)") as m:
            m.media(random_photo_url)
    except:
        with response.message("404 Mars not found. Here's one anyway :)") as m:
            m.media(default_image)

    return str(response)

app.run(debug=True)
