# django imports
from django.conf import settings

# elasticsearch imports
from elasticsearch import Elasticsearch

INDEX = settings.ELASTIC_SEARCH_CONFIG['INDEX']
HOST = settings.ELASTIC_SEARCH_CONFIG['HOSTS']


class MyElasticsearch(object):
    """
    Elasticsearch client for Leads app
    """
    def __init__(self, index=INDEX, host=HOST):
        """
        """
        self.index_name = index
        self.data_doc_type = 'my_data'
        self.client = Elasticsearch(host)

    def update_data(self, body, id, *args, **kwargs):
        """
        This method updates the data in the elasticsearch index
        """
        self.client.index(
            index=self.index_name,
            body=body,
            id=id,
            doc_type=self.data_doc_type
        )
