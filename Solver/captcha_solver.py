"""
HCaptcha ai solver.
Made by https://github.com/its-vichy.

For the moment captcha was detected, but ai work fine. So tokens lock,
I think py-hcaptcha update can do the trick.

Credit to:
    - https://github.com/h0nde/py-hcaptcha for library to get images and submit.
"""

from tensorflow.keras.models import load_model
import cv2, os, json, hcaptcha
import numpy as np

model = load_model('data.h5')
config =  json.load(open('./config.json'))

ch = hcaptcha.Challenge(
    site_key="4c672d35-0701-42b2-88c3-78380b0db560",
    site_url="https://discord.com",
    #proxy="user:pass@127.0.0.1:8888",
    #ssl_context=__import__("ssl")._create_unverified_context(),
    timeout=5
)

if ch.token:
    print(ch.token)
    exit()

os.system('cls')
print(ch.question["en"])

for tile in ch:
    image = tile.get_image(raw=True)

    img = cv2.imdecode(np.fromstring(image, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img,(config['image_size'],config['image_size']))
    img = np.expand_dims(img, axis=0)
    res = np.argmax(model.predict(img),axis=1)

    if res == 0:
        img_type = 'airplaine'
    if res == 1:
        img_type = 'bicycle'
    if res == 2:
        img_type = 'boat'
    if res == 3:
        img_type = 'motorbus'
    if res == 4:
        img_type = 'motorcycle'
    if res == 5:
        img_type = 'seaplane'
    if res == 6:
        img_type = 'train'
    if res == 7:
        img_type = 'truck'

    if img_type in ch.question["en"]:
        print(f'YES', img_type)
        ch.answer(tile)
    else:
        print('NO')

try:
    token = ch.submit()
    print(token)
except hcaptcha.ChallengeError as err:
    print(err)