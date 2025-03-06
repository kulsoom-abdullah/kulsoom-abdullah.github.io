End to End Recipe Cuisine Classification
========================================

AWS Lambda functions, BeautifulSoup, Python, Sci-Kit Learn
----------------------------------------------------------

[![Kulsoom Abdullah, PhD](https://miro.medium.com/v2/resize:fill:88:88/2*feWIsTg2YB9333UB0_F2Dg.jpeg)](https://medium.com/@liftingcovered?source=post_page---byline--e97f4ac22104---------------------------------------)

[![TDS Archive](https://miro.medium.com/v2/resize:fill:48:48/1*CJe3891yB1A1mzMdqemkdg.jpeg)](https://medium.com/towards-data-science?source=post_page---byline--e97f4ac22104---------------------------------------)

[Kulsoom Abdullah, PhD](https://medium.com/@liftingcovered?source=post_page---byline--e97f4ac22104---------------------------------------)



[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2Fdba469dcdc60&operation=register&redirect=https%3A%2F%2Fmedium.com%2Ftowards-data-science%2Fhttps-towardsdatascience-com-end-to-end-recipe-cuisine-classification-e97f4ac22104&user=Kulsoom+Abdullah%2C+PhD&userId=dba469dcdc60&source=post_page-dba469dcdc60--byline--e97f4ac22104---------------------post_header------------------)

Published in

[TDS Archive](https://medium.com/towards-data-science?source=post_page---byline--e97f4ac22104---------------------------------------)

14 min read

May 29, 2019

![Preparing Breakfast photo credit: Mark Weins @ https://migrationology.com/pakistan-travel-guide/](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*mrgzDmPgizfTNhvTcIy4sg.jpeg)

**Who should read this?**

If you are interested in learning about a high level overview of a Machine Learning system from scratch including:

— Data Collection (web scraping)

— Processing and cleaning the data

— Modeling, Training and Testing

— Deployment as a cloud service

— Scheduling to re-run the system, get any new recipes, and retrain the model

Introduction
============

Because of curiosity, desire to grow and learn — I decided to build an ML system from scratch covering everything from data collection and cleaning, modeling, training, and testing, as well deployment as a cloud service. That is, something applicable in real life.

I had found helpful articles on various parts of the pipeline but piecing the information together, getting further guidance from mentors and colleagues, and reading documentation to fill in knowledge gaps, took time. I decided to document my process in the hope it could help someone else out there who is googling ‘how to’ something my article could address.

This article will not be a tutorial of the tools I used, but will describe how I built this system and the decisions I made along the way, going with the lowest cost and simplest method to get the job done.

Overview
========

The overall project is described in two parts:

1.  The AWS pipeline
2.  Modeling work and results

All of the code is hosted on my GitHub repo [here](https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/tree/master/AWS-lambda-implementation).

_An upcoming third part will be on using AWS API to submit input data to the serialized model and send back a response (the prediction)._

Why recipe cuisine classification?
==================================

![Mark Weins @ https://migrationology.com/pakistan-travel-guide/](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*q4T4HK6jF9AH-qz9hCJfUw.jpeg)

Why did I choose to build a cuisine classifier? I like food. Growing up, I had both Northern Pakistani cuisine and the cuisine available in the USA cities I have lived in. I have always liked to try other cuisines so from friends and colleages from other countries outside of the USA, and when I get to travel, I have been exposed. How [global cuisine](https://en.wikipedia.org/wiki/Global_cuisine) has originated and developed over time is facincating. I notice the distinction and overlap of ingredients and methods, and how it has meshed and fused based on people migration and colonialism. Today, information is available on all types of food, and one can almost try any of it, without having to travel.

![Spices on Plate With Knife — Creative Commons Images https://www.pexels.com/](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*D_XlN2aDpXnVdU-3RQgewA.jpeg)

Business applications for this could be used in saving human moderation time in tagging incorrectly classified recipes, categorizing a new recipe for a database or archive.

Going Serverless with AWS Lambda Functions
==========================================

One of the reasons serverless architectures, such as AWS Lambda functions, are popular is not needing to manage a server in the cloud. In the words of [Amazon](https://aws.amazon.com/lambda/features/):

> AWS Lambda is a [serverless compute](https://aws.amazon.com/serverless/) service that runs your code in response to events and automatically manages the underlying compute resources for you. AWS Lambda can automatically run code in response to [multiple events](http://docs.aws.amazon.com/lambda/latest/dg/intro-core-components.html#intro-core-components-event-sources) …

The components I used were S3 buckets to write and retrieve data, a Simple Service Queue (SQS) to distribute the web scraping, and an API Gateway to handle the model endpoints.

Note: For the permissions, I set my [lambda functions to have full access](https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/blob/master/AWS-lambda-implementation/template.yaml) to the S3 buckets and SQS that I use. One can and should set a list of precise permission types for security reasons and avoid mishaps, especially in a setup with more moving parts.

Recipe Data Collection
======================

My goal was to classify a few cuisines and from one website that had a decent amount of recipes to work with. I ended up choosing [allrecipes.com](https://www.allrecipes.com), because it is popular and has a [moderation check](https://www.wikihow.com/Submit-a-New-Recipe-to-Allrecipes) for validity before a recipe is published. Without mention, there could be bias issues, such as distribution of the types of entrees within a cuisine, and issues such as misspellings, inauthentic or misplaced recipe to a cuisine. Business issue would be, is what is the data that it needs to predict on going to look like? Does the training data reflect that? I thought to start simply — what can I do with what I can get.

![allrecipes.com world cuisine page](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*2CZ7zFGoe_x9hwC6cQb4TA.png)

Each cuisine URL dynamically generates individual recipe links upon scrolling and these links are what I need to scrape. I wanted to distribute the scraping task of the 6 cuisines I chose into separate lambda invocations, and be under the 900 second limit. To accomplish this, I have the lambda function, [queue_cuisine_URLs.py](https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/blob/master/AWS-lambda-implementation/src/queue_cuisine_URLs.py) send the 6 cuisine URLs to a Simple Service Queue (SQS), _cuisine_URLs_ and this triggers the the lambda function, [scrape_html_links.py](https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/blob/master/AWS-lambda-implementation/src/scrape_html_links.py)_._ It firsts checks to see if a cuisine has already been scraped by getting any objects in the S3 bucket _recipe-url-page-numbers,_ otherwise starts scraping recipe URLs at page 1, and placing them in the _recipe-scraped-data_ S3 bucket.

![AWS Architecture Flowchart](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*UPyg7tEDfRSKclrmtIGCGw.png)

Then the`[parse_direct_URLs.py](https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/blob/master/AWS-lambda-implementation/src/parse_direct_URLs.py)` Lambda function scrapes the recipe text from the _recipe-scraped-data_ S3 bucket and puts them into the _recipes-allrecipes_ S3 bucket. The fields that I parse from each recipe are:

*   id
*   title
*   description
*   rating
*   reviews
*   ingredients

The recipe text parsing rules and model pipeline I decided on (described in section 2) were supported by Sagemaker and did not need to create a container to use my code. I created a [Sagemaker notebook instance](https://github.com/kulsoom-abdullah/kulsoom-abdullah.github.io/blob/master/AWS-lambda-implementation/model_implementation/Sagemaker%20recipe%20classification%20deployment.ipynb) with the Python code to parse the recipes, vectorize, and train the model. The model pipeline is pickled (serialized) and saved to an S3 bucket.

The entire flow starts again when the event trigger occurs on its regular schedule (every week), gets any new recipes, and retrains the model. The scale of the data is very small and model simple enough that I do not need to worry about storage issues of the training data, sampling a subset of the entire training data, or the time it takes to train on the data.

_In progress — serving the model using a static web page on S3 to take user input recipes, go to the AWS API, input to the model and get a prediction back. This blog post will be edited or a part 2 will be published next._

Modeling work
=============

Some of the questions I wanted to answer were:

*   Can recipes be classified from 6 different cuisines correctly using only their ingredients?
*   How well can I do for each of the classes, not just the average accuracy of all classes?
*   Is collecting more training data necessary or can I use alternative methods to work around this?

The binary case
===============

To get started and find out if it was worth moving forward with this project, I started with the [binary case](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+binary+classification%2Frecipe+binary+classification.html=).

Italian and Indian — polar opposites?
-------------------------------------

First attempt will be using indian and italian recipes, come up with rules to preprocess the ingredient list, and try out a simple BagofWords classifcation model. I start with Italian and Indian, as they seem to be contrasting cuisines for an easier problem, and the amount of recipes for these cuisines available were the highest.

[Parsing text rules](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+binary+classification%2Frecipe+binary+classification.html=#Words-to-Remove)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

— Weights and measures
----------------------

Weights and measures are the type of words, I expect, would not add value to the model (unless I was considering quantity as a feature, not just the ingredient word). Here is an example of a list of ingredients:

*   1 tablespoon vegetable oil
*   1/4 cup white sugar
*   1/4 teaspoon salt
*   2 cups all-purpose flour
*   2/3 cup water

As a result, this leaves these ingredient names: _vegetable oil, white sugar, salt, flour, and water_, hence the filtering.

**— Data leakages**
-------------------

Reviewing the ingredients, I saw words that would be potential data leakages and added them to my filtering list: ‘italianstyle’, ‘french’, ’thai’, ‘chinese’, ‘mexican’, ’spanish’, ’indian’, ’italian’

— Lemmatizing
-------------

Additionally, I lemmatize only, and chose not to stem words. This was to make it easier for me to understand ingredient significance and not have to go back and look up the unstemmed word if I could not recognize it. For example with, “1 sliced artichoke”, I want _artichoke_, not the [stemmed result](https://text-processing.com/demo/stem/) _artichok._ Doing this did not increase the number of distinct words.

— The rest
----------

That still leaves a lot of other words. There are advanced NLP techniques to recognize the entity of a word that would calculate the [probability that a word is the ingredient](https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/), while the rest are measures, textures, actions and other types of words that surround the ingredient word. Simply printing out the top most frequent words, and eyeballing which ones are useless to add to the filtering rules had great results and a relatively small set of unique words to vectorize, I went with this. Another reason is that doing this also saves a lot of time.

These final ingredient names are transformed using the [CountVectorizer library](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) in scikit-learn into a matrix of the words from the training set.

Class Counts
------------

![Count of Indian and Italian cuisines](https://miro.medium.com/v2/resize:fit:802/format:webp/1*paiGKfJhOAeqyrx_O8q6ug.png)

There are over 3 times more Italian than Indian recipes (2520 vs 787). Is it enough data for an ML model to learn what is Indian? Will the ML do better than 76% (a Dummy classifier where every recipe is classified as Italian)

_Multinomial Naive Bayes_
-------------------------

Using [Multinomial Naive Bayes](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+binary+classification%2Frecipe+binary+classification.html=#Naive-Bayes), which is simple and fast got almost “perfect” f1_weighted scores for both cuisines on the training and testing sets. The scores were consistent across 3 fold Stratified cross validation:

*   Average training score: 0.986
*   Average test score: 0.984

Since the the training and test scores are almost equal, overfitting is not a problem. Because the training score is not a perfect 1, we are underfitting. To decrease underfitting thereby increase the training score, the option is to increase the model complexity or use a more complex model. Future work could focus on using more complex models such as random forest. I stopped here because I was happy with this score and continued onto the multiclass case.

The Multiclass case
===================

![captionless image](https://miro.medium.com/v2/resize:fit:802/format:webp/1*Sb2p2kmF8CSJhgjUYjEfcw.png)

The work is in [this Jupyter Notebook](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=). The 6 classes are Chinese, French, Indian, Italian,Mexican, and Thai. The final results are in the [summary table](https://medium.com/p/e97f4ac22104#a249) below.

Related Work
------------

Some of the related work I found on recipe cuisine classification based on parsing ingredient text had similiar findings to my work. All of them did not have a balanced class dataset. [This team](http://cs229.stanford.edu/proj2015/313_report.pdf) had the best results with logistic regression due to their large training set. They found that upsampling the classes with small instance sizes did not yield better results. [This team](http://jmcauley.ucsd.edu/cse190/projects/fa15/022.pdf) used random forest and had better training scores vs regression on the training set, but overfit as the test results were worse. They had an accuracy score of 77.87% on 39,774 recipes. Neither team reports individual scores for each cuisine, but the overall accuracy on all cuisines.

[Initial Analysis](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Pipelines-and-K-fold-validation-to-compare-text-processing-and-models)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

I found that using bigrams gave the overall score some lift, and using count vectorizer vs the TFIDF has better results. This was expected based on the related work results and my domain knowledge of some of the cuisines. (Page 4 of [this paper](http://jmcauley.ucsd.edu/cse190/projects/fa15/022.pdf) gives an explanation of why tf idf was worse than count vectorizer for a recipe classification problem.) Due to these results, I changed my`parse_recipes` function to consider helpful two word ingredients into the document string and go with BagofWords.

Random forest overfits the data and Logistic Regression has a better results than Multinomial Naive Bayes due to the increase of data. I also checked the F1 scores by implementing each model and looking at the confusion matrix. The results are below and select models and the code are left [in the Jupyter notebook](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Recipe-Cuisine-Part-2---Multi-Classification).

![Initial results](https://miro.medium.com/v2/resize:fit:998/format:webp/1*8bHuIDPtFos8oP5umprLTg.png)

The best model performance is logistic regression with count vectorization which has an average test score of 0.870 and train score of 0.997. I proceed to analyze this model in more detail.

[Logistic Regression](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Logistic-Regression)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

As the data size grows, [Logistic Regression performs better than Naive Bayes](http://www.cs.cmu.edu/~tom/mlbook/NBayesLogReg.pdf). This is also true for the recipe dataset. Looking at the individual scores for each cuisine, there is overfitting, and it is not clear if class imbalance is a problem. For example, there are 75 total Mexican recipes with F1 score **=** 0.73, while there are 387 French recipes with F1 score 0**.**63**.**

![captionless image](https://miro.medium.com/v2/resize:fit:996/format:webp/1*-FdupU-zjvfBBf0-J9oKkw.png)![Logistic Regression train/test confusion matrix heat maps](https://miro.medium.com/v2/resize:fit:994/format:webp/1*MJzYqqb7wRHUui4y9k6OGg.png)

Some observations:

*   French mostly gets misclassified most as Italian
*   Mexican gets misclasified most as Italian
*   Thai as gets misclassified as Chinese followed by Indian.
*   Mexican as Italian is slightly unexpected but I can see why some of the printed cases.

> — One example where a mexican recipe was as italian:
> _plum oregano fish bouillon banana garlic tomato bouillon butter plum tomato onion olive oil black pepper caper olive bay salt oil pepper white fish pickled green olive cinnamon_

The scores for the training set are higher than the test, and I tried to deal with this overfitting and possible class imbalance contributions.

[Class weights in loss function](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Class-weights-in-loss-function)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The `[class_weight='balanced'](https://chrisalbon.com/machine_learning/logistic_regression/handling_imbalanced_classes_in_logistic_regression/)` argument will weigh classes inversely proportional to their frequency in the sci-kit learn Logistic Regression class. This gave a higher F1 average train score of 0.997 and test score of 0.892. There was some improvement with the individual classes that did not do as well without class weighted loss.

![captionless image](https://miro.medium.com/v2/resize:fit:1012/format:webp/1*4dA-gPhXMRiVA8YP0TkRPQ.png)![Logistic Regression (class weighted loss) train/test confusion matrix heat maps](https://miro.medium.com/v2/resize:fit:990/format:webp/1*VeQaL_WARaY5RZznLhYT3w.png)

[Oversampling and Undersampling](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Oversampling-and-Undersampling)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

I used a Python package called [Imbalance learn](https://imbalanced-learn.readthedocs.io/en/stable/) to implement over and undersampling, and find out if how much this would help or not help the scores of the cuisines.

![captionless image](https://miro.medium.com/v2/resize:fit:1012/format:webp/1*zrsVoEiF658SDsjEDqHzRw.png)![Logistic Regression (oversampling) train/test confusion matrix heat maps](https://miro.medium.com/v2/resize:fit:990/format:webp/1*ywdXOgPyUWCqGobPEj80Hw.png)

![captionless image](https://miro.medium.com/v2/resize:fit:1012/format:webp/1*ImF4EVNmH7Ycvd6fRkCtBg.png)![Logistic Regression (undersampling) train/test confusion matrix heat maps](https://miro.medium.com/v2/resize:fit:990/format:webp/1*QudeCVvTXcbba6gguGnnWg.png)

By comparison, oversampling did not make much difference except for reducing the Mexican score and French scores. Overall F1 train score was 1.0 and test score of 0.89. Undersampling had the worst performance with a training F1 score of 0.77 and testing F1 score of 0.75

[Chi-Squared](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Calculating-Chi-square-(%CF%87%C2%B2-)) (χ²)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Finally, using the χ² test for the ingredient features and selecting the top K significant ones is another method to deal with overfitting on the training set. Train F1 score was 0.934 and test F1 score was 0.866. The training scores went down slightly, and the test scores did not improve compared to the other models like Class Weighted Loss Function Logistic Regression.

![captionless image](https://miro.medium.com/v2/resize:fit:994/format:webp/1*v1DAURAcOFaITHcX0pClVA.png)![Logistic Regression (χ² 600 best) train/test confusion matrix heat maps](https://miro.medium.com/v2/resize:fit:992/format:webp/1*Wl350v5SsLMpYg5Xq75TbQ.png)

These are the top 10 ingredient words sorted by chi2 with class frequency:

1.  fish: 1897.8449503573233
    [(‘thai’, 48), (‘chinese’, 8), (‘indian’, 6), (‘french’, 5), (‘italian’, 4), (‘mexican’, 1)]
2.  cumin: 1575.1841574113994
    [(‘indian’, 275), (‘italian’, 16), (‘mexican’, 9), (‘thai’, 6), (‘chinese’, 1), (‘french’, 1)]
3.  husk: 1318.6409852859006
    [(‘mexican’, 12), (‘indian’, 3)]
4.  masala: 1236.5322033898303
    [(‘indian’, 146)]
5.  cheese: 1155.8931811338373
    [(‘italian’, 1074), (‘french’, 85), (‘indian’, 22), (‘mexican’, 9), (‘thai’, 3), (‘chinese’, 2)]
6.  fish sauce: 1119.2711018711018
    [(‘thai’, 45), (‘french’, 2), (‘chinese’, 2)]
7.  turmeric: 999.0619453767151
    [(‘indian’, 225), (‘thai’, 8), (‘italian’, 1)]
8.  peanut: 994.6422201344235
    [(‘thai’, 42), (‘chinese’, 26), (‘indian’, 24), (‘italian’, 3)]
9.  lime: 991.2019982362463
    [(‘thai’, 43), (‘indian’, 33), (‘mexican’, 17), (‘italian’, 8), (‘french’, 4), (‘chinese’, 3)]
10.  sesame: 958.9888557397035
    [(‘chinese’, 77), (‘indian’, 8), (‘italian’, 7), (‘thai’, 7), (‘french’, 1)]

The ingredent that had the highest score and most frequently appeared in the french was not until #66:

gruyere: 291.2451127819549
[(‘french’, 17), (‘italian’, 2)]

Deep Learning
=============

For fun and curiosity, I also implemented [two Deep Learning](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Appendix) architectures with Keras. The densely connected 2 layer network had a train F1 score of 0.996 and the best test F1 score by a tad above class weighted logistic regression with 0.8995.

In the second architecture I used with multichannel 2-gram with embedding and Conv1D, getting a train F1 score of 0.945 and Test F1 score of 0.8699. I wanted to try using bigrams to see how much difference that would make with the simple Deep Learning architecture . I found an [implementation here](https://machinelearningmastery.com/develop-n-gram-multichannel-convolutional-neural-network-sentiment-analysis/) that I used as a guide. I didnt think RNN would do much, like word2vec, because the order of ingredients is irrelevant to the cuisine.

![Final Results](https://miro.medium.com/v2/resize:fit:1210/format:webp/1*WXUEb8wQvXcTIDfPKMP1lg.png)

Experiment: Would more data help with overfitting, classes that do not score as high, and class imbalance?
==========================================================================================================

**[Edited June 1, 2019]**

I had collected a total of 4,177 data points — broken down by class: chinese = 260, french = 387, indian = 787, italian = 2520, mexican = 75, thai = 148. This led me to try [an experiment](https://htmlpreview.github.io/?https%3A%2F%2Fgithub.com%2Fkulsoom-abdullah%2Fkulsoom-abdullah.github.io%2Fblob%2Fmaster%2FAWS-lambda-implementation%2Fmodel_implementation%2Frecipe+multiclass+classification%2Frecipe+multiclass+classification.html=#Would-more-data-help-with-class-imbalance?) to test whether getting more data to balance the classes could make any improvement. This can be an important metric to quantify if getting more data is time consuming or expensive. It was not clear based on the results I had whether class imbalance contributes to low test scores.

I plotted what the test and training scores are, for each cuisine. The test data is fixed. The training class sizes start at 25 and continue in increments of 25. If the size is less then the class count, then it is downsampled to set them all equal. This is the case until the count goes over the class size.

![captionless image](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*u5qpnG1RwpQkKvhfmcrDbg.png)

Vertical colored lines mark the max class count on the x axis. Indian and Chinese peaks at about training size of 1000+ and flatlines to a little below this score. Mexican peaks earlier, at close to 500 and flatlines a bit below. Indian and Italian and French at around 1400, then tapers off to close the same score. Thai at 1300 and then also flatlines to close the same. I could go deeper by drawing more gridlines and getting the exact x value where the max f1 score occurs, but the general trend shows me that collecting more data would be helpful. The results of all of the other attempts in this notebook show that collecting more data is the last choice left in improving the training scores.

Summary of Results
==================

Conclusion summary
==================

*   Class Weighted had top scores for Chinese, French, Indian
*   Italian did the best with Conv1D and multigram embedding DL, followed by Class Weighted Logistic Regression.
*   Mexican did best with oversampling, followed by Class Weighted Logistic Regression.

The model, that I go with for the AWS deployment will be Class weighted loss function in Logistic Regression, the simplest and best overall. The decision for business can be based on how perfect of a classifier do you want, based on how quickly it trains and performs, how much data you have, and how does this need to work in production.

Other ideas in addition to collecting more data is considering the quantity of an ingredient as part of the feature weight.