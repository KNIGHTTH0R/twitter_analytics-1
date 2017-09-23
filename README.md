# Twitter Analytics

This is a personal POC project for twitter streaming, predicting the sentiment of kewords searched in twitter stream, and discover the current trending tags and topics.

Actually, the indent of the project is to get my hands dirty with verious tools. This projects integrates Kafka for message queuing, Spark Streaming for stream processing, ElasticSearch as a search engine and Kibana as a frontend and visualization tool, also Spacy for text preprocessing, Scikit-learn for features representation, Textblob for sentiment prediction.


## Installation

Clone the repo
```
git clone https://github.com/ahmedezzeldin93/twitter_analytics.git
```

You need first to install virtualbox and vagrant. Then 
```
cd twitter_analytics
vagrant up
```