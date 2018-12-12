from __future__ import print_function

import requests
from optimizely import optimizely
from optimizely.logger import SimpleLogger

class OptimizelyConfigManager(object):
  obj = None

  def __init__(self, sdk_key):
    print('Initializing local SDK with {}'.format(sdk_key))
    self.sdk_key = sdk_key

  def get_obj(self):
    if not self.obj:
      self.set_obj()
    return self.obj

  def set_obj(self, url=None):
    if not url:
      url = 'https://cdn.optimizely.com/datafiles/{0}.json'.format(self.sdk_key)

    datafile = self.retrieve_datafile(url)
    self.obj = optimizely.Optimizely(datafile, None, SimpleLogger())

  def retrieve_datafile(self, url):
    datafile = requests.get(url).text
    return datafile
