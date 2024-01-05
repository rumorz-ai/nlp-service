import asyncio
import unittest

from nlp_service.client import NLPService


class TestClient(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.nlp_service = NLPService()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.nlp_service.wait_for_start())

    def test_client(self):
        embeddings = self.loop.run_until_complete(self.nlp_service.get_embeddings("Your text here", source='app'))
        embeddings = self.loop.run_until_complete(self.nlp_service.get_embeddings("Your text here", source='local'))


    def test_nltk(self):
        loop = asyncio.get_event_loop()
        nlp_service = NLPService()
        nlp_service.nltk

