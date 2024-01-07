import asyncio
import os
import unittest

from nlp_service.client import NLPService
from smartpy.utility import os_util

os.environ['NLP_CACHE_DIR'] = os_util.getTempDir('nlp-service-cache')


class TestClient(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        nlp_service = NLPService(source=NLPService.API)
        self.loop.run_until_complete(nlp_service.check_api_status())

    def test_local_client(self):
        nlp_service = NLPService(source=NLPService.CACHE)
        embeddings = self.loop.run_until_complete(nlp_service.get_embeddings("Your text here"))
        self.assertTrue(len(embeddings) > 0)

    def test_api_client(self):
        nlp_service = NLPService(source=NLPService.API,
                                 base_url="http://0.0.0.0:80")
        #embeddings = self.loop.run_until_complete(nlp_service.get_embeddings("Your text here"))
        #self.assertTrue(len(embeddings) > 0)

    def test_nltk(self):
        loop = asyncio.get_event_loop()
        nlp_service = NLPService()
        nlp_service.nltk
