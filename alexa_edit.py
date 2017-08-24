#Some errors exist
from flask import Flask
from flask_ask import Ask,statement,question,session
import json,urllib
import time
import requests
from nutritionix import Nutritionix
nix = Nutritionix(app_id="app_id", api_key="app")

app = Flask(__name__)
ask= Ask(app,"/food_name")

def get_info(food):
	url="https://api.nutritionix.com/v1_1/search/food?results=0:10&fields=item_name,brand_name&appId=app_id&appKey=app_key"
	f=urllib.urlopen(url)
	values=json.load(f)
	f.close()
	results=[]
	for i_n in values['hits']['i_n']['fields']:
		results.append[{values['hits']['i_n']['fields']['item_name'],values['hits']['i_n']['fields']['brand_name']}]
	results='... '.join([i for i in results])
	return results

results=get_info("dosa")
print(results)

@app.route('/')
def homepage():
    return "Hi there! What's Up?"

@ask.launch
def start_skill():
    welcome_message = 'Hello there,would you name the food?'
    return question(welcome_message)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then,anyways...bye'
    return statement(bye_text)
@ask.intent("YesIntent")
def yes_intent():
	res='Please name the food for info'
	return statement(res)

@ask.intent("AnswerIntent")
def share_info(food):
    info = get_info(food)
    info_msg = 'The Item and the Brand names are'.format(info)
    return statement(info_msg)

if __name__ == '__main__':
    app.run(debug=True)
