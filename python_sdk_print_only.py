# 
# save the preceding code to a file like optimizely_print_demo.py
# run pip install optimizely-sdk
# run python optimizely_print_demo.py a few times
# then go look for results in the Optimizely app for your discount experiment  
# since your experiment is so brilliant, you'll see 100% of users who 
# got the discount made a purchase, and none who missed the discount did 
# https://app.optimizely.com/v2/projects/18139620475/results/18632340873/experiments/18637410992?previousView=EXPERIMENTS

import logging
import random
from optimizely import optimizely
from optimizely.helpers import enums

# Set log level to INFO
logging.basicConfig(level=logging.INFO)

#instantiate the Optimizely client
optimizely_client = optimizely.Optimizely(
                sdk_key='PnsTgkYA2fJUhHZRnZ9S5f'
                )

logging.info('Is optimizely_client valid: {}'.format(optimizely_client.is_valid))

# for demo purposes, generate random user ids so that the variation is re-evaluated every time
random.seed()
user_id = str(random.randrange(1001,9999))

#implement the flag
discount_enabled = optimizely_client.is_feature_enabled('discount', user_id)

# You'd use the follow info received from Optimizely to render your app
# For now, let's view logging statements 

if discount_enabled:  
      discount_amount = optimizely_client.get_feature_variable('discount', 'amount', user_id)
      logging.info('{} got a discount of {}'.format(user_id, str(discount_amount)))
      # hardcode user actions so we can see experiment results in the Optimziely app 
      # let's be wildly optimistic: people exposed to the discount are 100% more likely to purchase
      optimizely_client.track('purchase', user_id)
      logging.info('{} made a purchase'.format(user_id))
else:      
      logging.info('{} did not get the discount feature'.format(user_id))
      logging.info('{} did not make a purchase'.format(user_id))
