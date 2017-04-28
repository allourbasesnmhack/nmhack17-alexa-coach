import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr

def generateGoalsMessage(userid):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('goals')
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))

    items = response['Items']
    goal_message_bad=""
    goal_message_good=""

    for item in items:
        print item['goalname']

        diff= int(item['target'])-int(item['actual'])
        if(diff <= 0):
            diff=diff*-1
            if(item['goalname'] =='DailyGoal'):
                goal_message_good+=render_template('goal_item_over_daily', goalname=item['description'],actual=item['actual'],target=item['target'],difference=diff)
            else:
                goal_message_good+= render_template('goal_item_over', goalname=item['description'],actual=item['actual'],target=item['target'],difference=diff)
        else:
            if(item['goalname'] =='DailyGoal'):
                goal_message_good+=render_template('goal_item_under_daily', goalname=item['description'],actual=item['actual'],target=item['target'],difference=diff)
            else:
                goal_message_bad+= render_template('goal_item_under', goalname=item['description'],actual=item['actual'],target=item['target'],difference=diff)
    return goal_message_good+goal_message_bad
def generateGoalCard(userid):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('goals')
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))

    items = response['Items']
    card="<table><tr><th>Goal</th><th>Actual</th><th>Target</th></tr>";

    for item in items:
        card+="<tr><td>"+item['description']+"</td><td>"+item['actual']+"</td><td>"+item['target']+"</td></tr>"
    card+="</table>"
    return card
