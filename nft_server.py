# DOC : How to make this script work
# Step 1 : Request a Twitter API key on https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api
# Step 2 : Generate a user token for the app you just created on https://developer.twitter.com/en/portal/dashboard
# Step 3 : Store all your 5 secrets inside the file api_secrets.py

import api_secrets
import tweepy
import requests
from PIL import Image
from flask import Flask, send_file, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from io import BytesIO
from functools import lru_cache



client = tweepy.Client(bearer_token=api_secrets.BEARER_TOKEN,
                       consumer_key=api_secrets.API_KEY,
                       consumer_secret=api_secrets.API_KEY_SECRET,
                       access_token=api_secrets.USER_ACCESS_TOKEN,
                       access_token_secret=api_secrets.USER_ACCESS_TOKEN_SECRET)


mask_raw = Image.open('newmask.png')
assert mask_raw.size == (400, 400)
assert mask_raw.mode == 'RGBA'
mask_alpha = mask_raw.getchannel('A')
#mask = mask.resize((400, 400)).convert('RGBA')

def serve_png_image(pil_img):
    assert pil_img.size == (400,400)
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

#tweets = client.get_users_tweets(user_id, user_auth=True, tweet_fields=['public_metrics','non_public_metrics'])

@lru_cache(None)
def get_nft_picture(username):
    user = client.get_user(username=username, user_fields=['profile_image_url'])
    if user.data is None:
        return None
    pp_url = user.data.profile_image_url.replace('_normal','')
    
    r = requests.get(pp_url, stream=True)
    src = Image.open(r.raw)
    result = src.resize((400, 400))
    result.putalpha(mask_alpha)
    
    #result = Image.new('RGBA', (400, 400), (0, 255, 0, 0))
    #result = Image.composite(src, src, mask)
    
    return result
    

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["20 per hour", "5 per minute"]
)

@app.route("/nft/<username>")
def picture(username):
    nft_pic = get_nft_picture(username)
    if nft_pic is None:
        return 'Username does not exist'
    return serve_png_image(nft_pic)

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/nft/MathisHammel", code=302)

app.run(threaded=True, host='0.0.0.0', port=80)

