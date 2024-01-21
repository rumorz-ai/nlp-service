import asyncio
import os
import time
import traceback

import nltk
import aiohttp
import numpy as np
import requests
from aiohttp import ClientTimeout
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from smartpy.utility import os_util
from smartpy.utility.log_util import getLogger

SENTENCE_TRANSFORMERS_CACHE_DIR = os.path.join(os.path.dirname(__file__), 'sentence_transformers_cache')

NLTK_RESOURCES = ['brown', 'wordnet', 'stopwords', 'punkt', 'words', 'vader_lexicon']

logger = getLogger(__name__)

exceptions_to_retry = (requests.exceptions.Timeout,
                       asyncio.TimeoutError)


# Lazy loading function
def load_embedding_model(model, cache_folder=SENTENCE_TRANSFORMERS_CACHE_DIR):
    if not hasattr(load_embedding_model, "model"):
        from sentence_transformers import SentenceTransformer
        load_embedding_model.model = SentenceTransformer(
            model,
            cache_folder=cache_folder
        )
    return load_embedding_model.model


class NLPService:
    CACHE = 'cache'
    API = 'api'

    """
    This class is used to run NLP tasks, manage NLP libraries and model caching
    and interact with the NLP microservice.
    Libraries included:
    - NLTK
    - Sentence Transformers: get_embeddings
    """

    def __init__(self,
                 source=None,
                 base_url='http://0.0.0.0:80'):
        self.source = source
        self.base_url = base_url
        self.nltk_downloaded = False
        self.nlp_cache_dir = os.environ.get('NLP_CACHE_DIR', os_util.getTempDir('nlp-service-cache'))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        retry=retry_if_exception_type(exceptions_to_retry)
    )
    async def _async_request(self, endpoint, data={}, timeout_seconds=10):
        timeout = ClientTimeout(total=timeout_seconds)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(self.base_url + '/' + endpoint, json=data) as response:
                return await response.json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        retry=retry_if_exception_type(exceptions_to_retry)
    )
    def _request(self, endpoint, data={}, timeout_seconds=10):
        url = self.base_url + '/' + endpoint
        response = requests.post(url, json=data, timeout=timeout_seconds)
        response.raise_for_status()
        return response.json()


    def _is_running(self):
        try:
            result = self._request('ping')
            if result['status'] == 'success':
                return True
            else:
                return False
        except Exception as e:
            logger.debug(traceback.format_exc(e))
            return False

    def check_api_status(self,
                         n_trials=3):
        if self.source == self.CACHE:
            return True
        i = 0
        while i < n_trials:
            i += 1
            logger.info(f"Checking if NLP services are running... {i}")
            logger.info(f"Base URL: {self.base_url}")
            logger.info(f"Source: {self.source}")
            if self._is_running() is True:
                logger.info("NLP services are running")
                return True
            else:
                logger.info("Waiting for NLP services to start...")
                time.sleep(10)
            if i == n_trials:
                raise Exception("NLP services not running")

    def _download_nltk(self,
                       resources=NLTK_RESOURCES):
        # Set NLTK_DIR to the current_dir
        os_util.ensureDir(self.nlp_cache_dir)
        nltk.data.path.append(self.nlp_cache_dir)
        for res in resources:
            nltk.download(res, download_dir=self.nlp_cache_dir)

    @property
    def nltk(self):
        if not self.nltk_downloaded:
            self._download_nltk()
            self.nltk_downloaded = True
        return nltk


    async def get_embeddings(self,
                             text,
                             model='sentence-transformers/all-MiniLM-L6-v2') -> np.array:
        if self.source == self.API:
            data = {
                'text': text,
                'model': model,
            }
            response = await self._async_request(endpoint='embeddings', data=data)
            if response['status'] != 'success':
                raise ValueError(f'Error in response: {response}')
            else:
                return [np.array(i) for i in response['data']['embeddings']]
        elif self.source == self.CACHE:
            model = load_embedding_model(model=model)
            return model.encode(text)
