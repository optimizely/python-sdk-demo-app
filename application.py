# Python SDK Demo App
# Copyright 2016 Optimizely. Licensed under the Apache License
# View the documentation: http://optimize.ly/py-sdk
from __future__ import print_function

import csv
import json
import os
from operator import itemgetter
import random

from optimizely_config_manager import OptimizelyConfigManager
from http_rpc_client import Optimizely as OptimizelyRPC

from flask import Flask, render_template, request

# update SDK_KEY
SDK_KEY = os.getenv('SDK_KEY')
CLOUDFLARE_HOST = os.getenv('CLOUDFLARE_DECISION_SERVICE', 'http://tyler.ocdndns.com')
DECISION_SERVICE_HOST = os.getenv('DECISION_SERVICE_HOST', 'http://localhost:9090')
DECISION_SERVICE_GPRC_HOST = os.getenv('DECISION_SERVICE_GRPC_HOST', 'http://localhost:1337')

application = Flask(__name__, static_folder='images')
application.secret_key = os.urandom(24)

config_manager = OptimizelyConfigManager(SDK_KEY)


def build_items():
  items = []
  reader = csv.reader(open('items.csv', 'r'))
  for line in reader:
      items.append({'name': line[0],
                      'color': line[1],
                      'category': line[2],
                      'price': int(line[3][1:]),
                      'imageUrl': line[4]})
  return items

def index_handler(optly_factory, title):
  user_id = str(random.random())

  items = build_items()

  optly = optly_factory()
  if optly.is_feature_enabled('banner', user_id):
    variation_key = optly.get_feature_variable_string('banner', 'message', user_id)
  else:
    variation_key = False

  return render_template('index.html', data=items, variation_key=variation_key, title=title)

# render homepage
@application.route('/')
def index():
  return index_handler(lambda: config_manager.get_obj())

@application.route('/local-sdk')
def local_sdk():
  return index_handler(lambda: config_manager.get_obj(), title='Local SDK')

@application.route('/cloudflare-sdk')
def cloudflare_sdk():
  return index_handler(lambda: OptimizelyRPC(SDK_KEY, CLOUDFLARE_HOST), title='Cloudflare Worker')

@application.route('/decision-service')
def decision_service():
  return index_handler(lambda: OptimizelyRPC(SDK_KEY, DECISION_SERVICE_HOST), title='Decision Service')

@application.route('/decision-service-grpc')
def decision_service_grpc():
  raise NotImplementedError
  # return index_handler(lambda: OptimizelyRPC(SDK_KEY, DECISION_SERVICE_GRPC_HOST), title='Decision Service (GRPC)')

# display items
@application.route('/shop', methods=['GET', 'POST'])
def shop():
  user_id = request.form['user_id']

  # compute variation_key
  variation_key = config_manager.get_obj().activate('<experiment_key>', user_id)

  # load items
  sorted_items = build_items()

  # sort by price
  if variation_key == 'price':
    print("In variation 1")
    sorted_items = sorted(sorted_items, key=itemgetter('price'))

  # sort by category
  if variation_key == 'category':
    print("In variation 2")
    sorted_items = sorted(sorted_items, key=itemgetter('category'))

  return render_template('index.html',
    data=sorted_items, user_id=user_id, variation_key=variation_key)

# process a purchase event
@application.route('/buy', methods=['GET', 'POST'])
def buy():
  user_id = request.form['user_id']

  # track conversion event
  config_manager.get_obj().track("<event_key>", user_id)

  return render_template('purchase.html')

# webhook logic
@application.route('/webhook', methods=['POST'])
def webhook_event():
  data = request.get_json()

  event_type = data['event']
  # use CDN URL from webhook payload
  if event_type == 'project.datafile_updated':
      url = data['data']['cdn_url']
      config_manager.set_obj(url)
      return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

  return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

if __name__ == '__main__':
  application.debug = True
  application.run(port=4001)
