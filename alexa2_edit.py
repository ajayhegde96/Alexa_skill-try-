#Generate Cricket news top 10 headlines from reddit
from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/cric_news")

def get_headlines():
    user_pass_dict = {'user': 'username',
                      'passwd': 'password',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'Cric news'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://www.reddit.com/r/Cricket/new/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles
ti=get_headlines()
print(ti)

@app.route('/cric_news')
def homepage():
    return get_headlines()
@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like the  cricket news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current cricket news headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("HelpIntent")
def no_intent():
    help_text = 'Start by saying ...Alexa Ask cricket tops to start and answer with yes or no to continue...Would you like the cricket news?'
    return question(help_text)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Too bad, but cricket is good though... bye'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)
