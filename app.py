from random import choice

from flask import Flask, request, redirect
import requests

rover_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'

app = Flask(__name__)


@app.route('/img', methods=['GET'])
def get_mars_img():
    sol = request.args.get('sol')
    request_params = {'api_key': 'DEMO_KEY', 'sol': sol}

    response = requests.get(rover_url, params=request_params).json()
    photos = response['photos']
    random_photo_url = choice(photos)['img_src']

    return random_photo_url

app.run(debug=True)
