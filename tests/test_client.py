import asyncio
import unittest

from nlp_service.client import NLPService
from smartpy.utility import os_util


class TestClient(unittest.TestCase):

    def test_client(self):
        loop = asyncio.get_event_loop()
        nlp_service = NLPService()
        embeddings = loop.run_until_complete(nlp_service.get_embeddings("Your text here", source='app'))
        embeddings = loop.run_until_complete(nlp_service.get_embeddings("Your text here", source='local'))

        os_util.listDir(nlp_service.sentence_transformers_cache_dir)
        print(embeddings)
