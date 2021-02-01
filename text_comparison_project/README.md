#  Text Comparison Project

* [General info](#general-info)
* [URL](#url)
* [Commands](#commands)

##  General info

This project consists of a primary Python script and a Flask app built in a docker container. The docker container can be accessed from docker push madirajurv/develop:text_comparison

The Python script takes 2 strings of text as input from text entry boxes using a POST method. The script then outputs the similarity score which is represents represents a score between 0 and 1 based on the number of words that are common between both texts per sentence and the total number of words in the sentence when each sentence has more than 75% of the same words. 

The project uses Flask for the web services, uses an index.py to handle URL requests and a HTML template file to generate the webpage with text request forms and outputs from the script/

## URL

To see if Flask app is running:

> http://localhost:5000

To input texts:

> http://localhost:5000/compare_texts

To look at score or error messages resulting from text input:

> http://localhost:5000/compare_text_info

## Commands

With Docker:

$ docker pull madirajurv/develop:text_comparison
$ docker run -d -p 5000:5000 madirajurv/develop:text_comparison
