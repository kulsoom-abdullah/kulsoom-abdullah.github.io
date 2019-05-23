# lambda handler that is triggerd by content written to the S3 bucket, recipe-scrape-data
from botocore.vendored import requests
from bs4 import BeautifulSoup
import json
import re
import boto3
import time
import botocore


def lambda_handler(event, context):
    """
    This lambda function is used to scrape a direct URL.
    :param event: It is triggered by a PUT to the recipe-scraped-data S3 bucket.
    :param context:
    :return: nothing
    """

    # Object Information parsing from S3 Event Trigger

    records = [x for x in event.get('Records', []) if x.get('eventName') == 'ObjectCreated:Put']
    sorted_events = sorted(records, key=lambda e: e.get('eventTime'))

    latest_event = sorted_events[-1] if sorted_events else {}
    info = latest_event.get('s3', {})
    file_key = info.get('object', {}).get('key')
    bucket_name = info.get('bucket', {}).get('name')

    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name,
                         file_key,
                         '/tmp/' + file_key
                         )
        time.sleep(2)
    except botocore.exceptions.ClientError as e:
        print(e)

    with open('/tmp/' + file_key) as f:
        recipe_data = json.load(f)
        # parse json recipes file
        url_list=recipe_data['RecipeURLs']

    for url in url_list:
        url, cuisine = url.split(',')
        get_recipe_info(url, cuisine)


def get_recipe_info(url, cuisine):
    '''

    :param url: direct url for a recipe on AllRecipes.com
    :param cuisine: the type of cuisine
    :return: None
    This function scrapes a recipe given the URL, passes the content to the add_recipe function which
    places it into "recipes-allrecipes" S3 bucket
    '''
    ingredients_list = []

    # cuisine = url_cuisine[1]

    print(url, cuisine)
    page = requests.get(url)
    content = BeautifulSoup(page.text, "html.parser")

    # Get ID of recipe
    body = content.find('body')

    try:
        body_dict = json.loads(body['data-scoby-impression'])
    except KeyError as e:
        #print(e)
        print("{0} does not have scoby and no recipe to scrape".format(url))
        return #get out of function and go to next URL

    recipe_id = body_dict['id']

    # Get title of recipe
    title = content.title
    recipe_title = title.text.strip()

    # Get description of recipe
    description = content.find('div', {'class': 'submitter__description'})
    recipe_description = description.text.strip().replace('"', '')

    # Get list of ingredients for recipe
    for recipe_ingredients in content.find_all('label', title=True):
        ingredients_list.append(recipe_ingredients['title'])

    ingredients = ','.join(ingredients_list)

    htmlRating = content.find_all('span', {'itemprop': 'aggregateRating'})
    strRating = re.search('(?<=content=")(.*)(?=" itemprop="ratingValue")',
                          str(htmlRating)).group(1)
    strReviews = re.search('(?<=content=")(.*)(?=" itemprop="reviewCount")',
                           str(htmlRating)).group(1)

    add_recipe(recipe_id, recipe_title, recipe_description, strRating, strReviews,
               list(set(ingredients_list)), url, cuisine)


def add_recipe(recipe_id, recipe_title, recipe_description, strRating, strReviews, ingredients_list, url,
               cuisine):
    s3 = boto3.client('s3')
    bucket_name = "recipes-allrecipes"

    recipe_json = {'id': recipe_id,
                   'title': recipe_title,
                   'description': recipe_description,
                   'rating': strRating,
                   'reviews': strReviews,
                   'ingredients': ingredients_list,
                   'url':  url,
                   'category': cuisine,
                   }
    with open('/tmp/recipe.json', 'w') as f:  # writing JSON object
        json.dump(recipe_json, f)
    # print("scraped a recipe url for id {0}".format(recipe_title))
    s3.upload_file('/tmp/recipe.json', bucket_name, recipe_id + "-" + cuisine + ".json")

