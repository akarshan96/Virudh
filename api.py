from flask import Flask
from flask import Response as response
from flask import request
from flask_cors import CORS
from soft_tests import perform_soft_tests
from hard_tests import perform_hard_tests
from sentiment_analysis import perform_sentiment_test
import json
import pymongo

app = Flask(__name__)
CORS(app)


@app.route("/soft_tests", methods=['POST', 'GET'])
def soft_tests():
    print(request)
    news_text = request.args['news']
    return_dict = perform_soft_tests(news_text)
    resp = response(json.dumps(return_dict))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/hard_tests", methods=['POST', 'GET'])
def hard_tests():
    news_text = request.args['news']
    return_dict = perform_hard_tests(news_text)
    resp = response(json.dumps(return_dict))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/both_tests", methods=['POST', 'GET'])
def both_tests():
    news_text = request.args['news']
    return_dict = perform_soft_tests(news_text)
    links_list = perform_hard_tests(news_text)
    sentiment_list = perform_sentiment_test(news_text)
    return_dict['links'] = links_list
    return_dict['sentiments'] = sentiment_list
    resp = response(json.dumps(return_dict))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    print(resp)
    return resp

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

# Congress president Rahul Gandhi on sunday said the government would be able to instil faith among the young only by competing with China in creating jobs, and asserted the issue would be the central theme for India in the coming years.
