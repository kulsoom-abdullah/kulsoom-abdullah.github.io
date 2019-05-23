
import requests
from bs4 import BeautifulSoup
import json
import re
import boto3
import time
import collections


s3 = boto3.client('s3')
sqs = boto3.resource('sqs')
bucket_name = "recipe-scraped-data"  # Replace it with your own bucket name
bucket_page_state = "recipe-url-page-numbers"
timestr = time.strftime("%Y%m%d-%H%M%S")


# def get_recipe_urls(start_url, cuisine):
def get_recipe_urls(url_cuisine_tuple):
    start_url = url_cuisine_tuple[0]
    cuisine = url_cuisine_tuple[1]

    print("scraping for {0}".format(cuisine))

    # write if cuisine page object doesnt exist, then start page is 1, else get last page scraped

    start_page = 0
    key = "{0}-last-page.txt".format(cuisine)
    objs = s3.list_objects_v2(Bucket=bucket_page_state)
    try:
        if len(objs) > 0:
            for name in objs['Contents']:
                if key == name['Key']:
                    print("Exists!")
                    obj = s3.get_object(Bucket=bucket_page_state, Key=key)
                    j = json.loads(obj['Body'].read().decode('utf-8'))
                    print(j['page'])
                    start_page=int(j['page'])
    except KeyError:
        print("No objects in the s3 bucket")

    for i in range(start_page, 2828):  # 2828 is a count that currently shouldn't exceed a cuisine

        url_page = "{0}?page={1}".format(start_url, str(i))
        #print(url_page)
        page = requests.get(url_page)
        time.sleep(3)
        content = BeautifulSoup(page.content, 'html.parser')

        num_recipes = len(content.find_all('article', {'class': 'fixed-recipe-card'}))
        if num_recipes == 0:
            print("page {0} is the last with no recipes returned".format(i))
            cuisine_page = {
                'cuisine': cuisine,
                'page': i}
            with open('/tmp/page.json', 'w') as f:  # writing JSON object
                json.dump(cuisine_page, f)
            s3.upload_file('/tmp/page.json', bucket_page_state, key)
            break
        s3_result_dump = collections.defaultdict(list)
        # Get a list of URLs
        for recipes in content.find_all('article', {'class': 'fixed-recipe-card'}):
            for recipe in recipes.find_all('div', {'class': 'fixed-recipe-card__info'}):
                for url in recipe.find_all('a', {'class': 'fixed-recipe-card__title-link'}):
                    # url_list.append([url['href'], cuisine])

                    url_cuisine = url['href'] + "," + cuisine
                    s3_result_dump['RecipeURLs'].append(url_cuisine)

                    with open('/tmp/urls.json', 'w') as outfile:
                        json.dump(s3_result_dump, outfile)
        s3.upload_file('/tmp/urls.json', bucket_name, "RecipeURLs_"+cuisine +"_pg"+ str(i)+ "-" + timestr + ".json")



def lambda_handler(event, context):
    '''

    :param event: SQS item addition
    :param context: None
    :return: Nothing
    This lambda function is triggered by strings added to the cuisine_URLs SQS
    '''

    url_cuisine_extract = event["Records"][0]['messageAttributes']['url_cuisine']['stringValue']

    print(url_cuisine_extract.split(','))
    get_recipe_urls(url_cuisine_extract.split(','))
