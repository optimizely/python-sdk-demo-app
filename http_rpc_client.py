from __future__ import print_function

import json
import sys

# https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application

import requests
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class Optimizely(object):
  def __init__(self, sdk_key, decision_service_host):
    print('Initializing RPC client with host: {} and SDK key: {}'.format(decision_service_host, sdk_key))
    self.sdk_key = sdk_key
    self.rpc_url = '{}/rpc'.format(decision_service_host)

  def _construct_feature_payload(self, feature_key, user_id, variable_key=None, variable_type='string', attributes=None):
    data = {
      'features': {
        'feature_key': feature_key,
        'user_id': user_id,
        'datafile_key': self.sdk_key,
        # TODO(tyler): this is required by the RPC endpoint but we don't really use it
        'feature_config': {},
      }
    }
    if variable_key:
      data['features']['feature_config'][variable_key] = variable_type

    if attributes:
      data['features']['attributes'] = attributes

    return data

  def is_feature_enabled(self, feature_key, user_id, attributes=None):
    data = self._construct_feature_payload(feature_key, user_id, attributes=attributes)

    print('Sending data to RPC {}: {}'.format(self.rpc_url, json.dumps(data)))
    resp = requests.post(self.rpc_url, json=data)
    print('Got response from features: {}'.format(resp))
    if resp.status_code == 200:
      resp_data = resp.json()
      print('Response data: {}'.format(json.dumps(resp_data)))
      return resp_data['features']['is_enabled']
    else:
      return False

  def get_feature_variable_string(self, feature_key, variable_key, user_id, attributes=None):
    data = self._construct_feature_payload(feature_key, user_id, variable_key=variable_key, attributes=attributes)

    print('Sending data to RPC {}: {}'.format(self.rpc_url, json.dumps(data)))
    resp = requests.post(self.rpc_url, json=data)
    print('Got response from features: {}'.format(resp))
    if resp.status_code == 200:
      resp_data = resp.json()
      print('Response data: {}'.format(json.dumps(resp_data)))
      return resp_data['features']['feature_config'][variable_key]
