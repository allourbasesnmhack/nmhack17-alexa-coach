import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr

def generateGoalsMessage(userid):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('goals')
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))

    items = response['Items']
    goal_message= ""
    for item in items:
        print item['goalname']
        diff= int(item['target'])-int(item['actual'])
        if(diff <= 0):
            diff=diff*-1
            goal_message+= render_template('goal_item_over', goalname=item['description'],actual=item['actual'],target=item['target'],difference=diff)
        else:
            goal_message+= render_template('goal_item_under', goalname=item['description'],actual=item['actual'],target=item['target'],difference=diff)
    return goal_message