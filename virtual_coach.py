import logging
import boto3
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def start_skill():
    #welcome_message = render_template('welcome')

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('users')

    response = table.get_item(
        Key={
            'username': 'normweston',
            'last_name': 'Weston'
        }
    )

    item = response['Item']
    #firstname = item['first_name']
    #print(item['first_name'])
    #welcome_message = item['first_name']
    welcome_message = 'Welcome ' + item['first_name'] + ' ' + item['last_name'] + ' to the North Western Mutual Virtual Coach.'
    welcome_message = welcome_message + '''
                      Here is your daily summary of activity.
                      Norm, you have a total of 5 open activities for today.
                      You have 3 fact finding.
                      You have 2 qualified suspect.
                      Would you like to hear your goals tracking?
                      '''
    return question(welcome_message)

@ask.intent("YesIntent")
def yes_intent():
    yes_message = 'Norm, you are over you goals by 5 activities'
    return statement(yes_message)

@ask.intent("NoIntent")
def no_intent():
    no_message = 'See you tomorrow.  Have a good day!'
    return statement(no_message)

if __name__ == '__main__':
    app.run(debug=True)
