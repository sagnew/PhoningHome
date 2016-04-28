import requests

rover_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
parameters = {'api_key': 'DEMO_KEY', 'sol': '1324'}

response = requests.get(rover_url, params=parameters).json()

print(len(response['photos']))
for photo in response['photos']:
    print(photo['img_src'])
