# Python SDK Demo App

This demo uses the Python SDK, a part of Optimizely's Full Stack solution. It will walk you through:

1. How to bucket users into experiment variations 
2. How to track conversion events
3. How to view the experiment’s results 
4. How to receive experiment updates via webhooks

## Optimizely Full Stack Overview

Optimizely Full Stack allows developers to run experiments anywhere in their code! The Python SDK provides the core components to run a full stack experiment with Optimizely. It handles aspects like bucketing, which is used to designate users to a specific experiment variation, conversion tracking, and reporting via Optimizely’s [Stats Engine](https://www.optimizely.com/statistics/).  

* View the [Python Getting Started Guide](http://developers.optimizely.com/server/getting-started/index.html?language=python)

* View the reference [documentation](http://developers.optimizely.com/server/reference/index.html?language=python).

* Latest [Python SDK](https://github.com/optimizely/python-sdk)

## Demo App

This example app simulates an online retailer testing the effects of sorting products by price vs category.

Using the instructions below, you can run the app locally and mimic bucketing website visitors by entering unique user IDs into the search bar. For example, the user ID “Matt” would simulate a unique visitor and select a specific variation for that unique visitor. The variation that is given to a specific unique visitor, such as Matt, will be deterministic. This means as long as the experiment conditions remain the same, Matt will always get the same variation.
 
<img src="https://github.com/optimizely/python-sdk-demo-app/blob/master/images/screenshot.png" width="420" height="369px">

### Deploying the App
1. Login or create an [Optimizely Account](https://app.optimizely.com/signin).
2. Setup a Python project via the Optimizely dashboard. [Instructions](http://developers.optimizely.com/server/getting-started/index.html?language=python)
3.  Create and run a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
4. In `application.py`, update the `project_id`, `experiment_key`, variation keys, and `event_key` where appropriate in code.
5. Install requirements: `pip install -r requirements.txt`
6. Run the application `python application.py` (be sure the virtualenv is running)
7. You’re all set. Play around and view the experiment's results! 

To better understand this experiment, we recommend you bucket a few different visitors into variations and simulate a conversion event by clicking the Buy Now button. Within a few seconds, you should see the results populate on the Optimizely results page. 

Note: The webhook service should be used to determine when changes have been made to an experiment. A test script, `test_webhook.py`, has been provided to mimic a webhook event. If you run this file (`python test_webhook.py`) it will send a POST request with a sample webhook payload. Before running, update the `project_id` on line 4.  

### Building the App


First, we must initialize the Optimizely Python SDK. The `optimizely_config_manager.py` module handles setting the Optimizely client, as well as returning it. To instantiate an Optimizely client you must pass in a [datafile](http://developers.optimizely.com/server/reference/index.html#datafile). The datafile acts as a config file and represents the state of your Optimizely project. It contains information like the status of your experiments and variation traffic allocation. The `set_obj` function, retrieves the datafile and initializes an Optimizely object. 

```python

url = 'https://cdn.optimizely.com/json/{0}.json'.format(self.project_id)
datafile = self.retrieve_datafile(url)
self.obj = optimizely.Optimizely(datafile)
```    
The crux of this Full Stack experiment is bucketing users into variations and exposing them to different sorting functions. The SDK’s `activate()` function will bucket users into a variation based on a user ID (internal id, user cookie, etc…). Below we use the variation key, returned by the SDK, to branch into a sorting algorithm based on price or category.   

```
variation_key = config_manager.get_obj().activate(‘item-sort’', user_id)

# sort by price
  if variation_key == 'price':
    sorted_items = sorted(sorted_items, key=itemgetter('price'))

  # sort by category
  if variation_key == 'category':
    sorted_items = sorted(sorted_items, key=itemgetter('category'))

```
To actually test which sorting algorithm influences increased sales, we need to track the number of clicks on the Buy Now button. We can leverage the `track()` function, which is subsequentlly called from the `buy()` function in `application.py`. To match the variation with the conversion event we must pass in the user_id. 

```
  # Track conversion event
  config_manager.track("item_purchase", user_id)
``` 

Lastly, let’s take a look at the `webhook_event()` endpoint. The webhook service alerts your application via an HTTP POST request when any changes are made to the project. You should provide your endpoint URL via the web app in Settings -> Webhooks. This is useful to ensure that your experiments are updated when you make changes in the web portal. The request will look like this: 

```
"timestamp":1463602412,
"project_id":1234,
"data":{  
   "cdn_url":"https://cdn.optimizely.com/json/1234.json",
   "origin_url":"https://optimizely.s3.amazonaws.com/json/1234.json",
   "revision":15
},
"event":"project.datafile_updated"
```
Our endpoint looks at the event type and then re-initializes the Optimizely object with this new Datafile --- again, this is handled by the `OptimizelyConfigManager` class. As mentioned above, you can use the `test_webhook.py` script to mimic webhook events. 

## Getting Help! 

* Developer Docs: http://developers.optimizely.com/server
* Questions? Shoot us an email at developers@optimizely.com
