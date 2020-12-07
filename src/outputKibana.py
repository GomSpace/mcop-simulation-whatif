#! /usr/bin/env python3

""" Call ElasticSearch AWS """

#Import ES library
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

#Import ORCHESTRATOR file managment

host = 'https://search-hoopsim-xebvo4edd36kgunyxhaxct2tqi.eu-central-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'eu-central-1' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}

es.index(index="movies", doc_type="_doc", id="5", body=document)

print(es.get(index="movies", doc_type="_doc", id="5"))

# -*- coding: utf-8 -*-

