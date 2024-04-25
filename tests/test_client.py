import asyncio
import unittest

from nlp_service.client import NLPService
from rumorz_llms.constants import nlp_service


class TestClient(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        nlp_service.check_api_status()

    def test_client(self):
        embeddings = nlp_service.get_embeddings("Your text here")
        self.assertTrue(embeddings)

    def test_nltk(self):
        nlp_service = NLPService()
        nlp_service.nltk

