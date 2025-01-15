import json

def lambda_handler(event, context):
    try:
        # Decode the JSON body from the HTTP event
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event  # For testing directly without a function URL

        # Parse input numbers
        number1 = body.get('number1')
        number2 = body.get('number2')

        # Ensure the numbers are provided
        if number1 is None or number2 is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Both number1 and number2 are required in the request.')
            }

        # Ensure the inputs are numbers
        if not isinstance(number1, (int, float)) or not isinstance(number2, (int, float)):
            return {
                'statusCode': 400,
                'body': json.dumps('Both number1 and number2 must be numbers (int or float).')
            }

        # Calculate the sum
        result = number1 + number2

        # Return the result
        return {
            'statusCode': 200,
            'body': json.dumps({'result': result})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }