# This is the first lambda function in the process of scraping recipes.
# it is triggered on a schedule

import boto3

sqs = boto3.resource('sqs')


def lambda_handler(event, context):
    """
    - This lambda function sends each element of a cuisine type (url, category) to a SQS
    - The elements are joined by a comma and the value sent is a string
    - The lambda function, scrape_html_links.py, is triggered by these inserts to the SQS URL
    - The purpose is to distribute the scraping task of each cuisine into separate lambda operations
    and be under the 900 second limit
    """

    cuisine_tuple = [("https://www.allrecipes.com/recipes/1470/world-cuisine/latin-american/mexican", "mexican"),
                     ("https://www.allrecipes.com/recipes/721/world-cuisine/european/french", "french"),
                     ("https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian", "indian"),
                     ("https://www.allrecipes.com/recipes/723/world-cuisine/european/italian", "italian"),
                     ("https://www.allrecipes.com/recipes/702/world-cuisine/asian/thai/", "thai"),
                     ("https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese", "chinese")
                     ]
    queue = sqs.get_queue_by_name(QueueName='cuisine_URLs')

    for tup in cuisine_tuple:
        url_cuisine = ','.join(tup)
        queue.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/495349584106/cuisine_URLs',
            MessageBody=url_cuisine,
            DelaySeconds=10,
            MessageAttributes={
                'url_cuisine': {
                    'StringValue': url_cuisine,
                    'DataType': 'String'
                }
            })
