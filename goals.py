def getGoalsMessage(userid):
    table = dynamodb.Table('goals')
    response = table.query(
        KeyConditionExpression=Key('userid').eq(userid)
    )
    items = response['Items']
    goal_message= ""
    for item in items:
        diff= item['target']-item['actual']
        goal_message+= render_template('goal_item', goal_name=item['goalname'],actual=item['actual'],target=item['target'],difference=diff)
    return goal_message
