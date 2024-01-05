import os
import nltk
import aiohttp

NLTK_CACHE_DIR = os.path.join(os.path.dirname(__file__), 'nltk_cache')
SENTENCE_TRANSFORMERS_CACHE_DIR = os.path.join(os.path.dirname(__file__), 'sentence_transformers_cache')

NLTK_RESOURCES = ['brown', 'wordnet', 'stopwords', 'punkt', 'words', 'vader_lexicon']
DEFAULT_EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'


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

    def __init__(self,
                 base_url='http://localhost:2222',
                 sentence_transformers_cache_dir=SENTENCE_TRANSFORMERS_CACHE_DIR,
                 nltk_cache_dir=NLTK_CACHE_DIR, ):
        self.base_url = base_url
        self.sentence_transformers_cache_dir = sentence_transformers_cache_dir
        self.nltk_cache_dir = nltk_cache_dir
        self.nltk_downloaded = False

    async def _send_request(self, endpoint, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url + '/' + endpoint, json=data) as response:
                return await response.json()

    def _download_nltk(self,
                       resources=NLTK_RESOURCES):
        # Set NLTK_DIR to the current_dir
        os.makedirs(self.nltk_cache_dir, exist_ok=True)
        nltk.data.path.append(self.nltk_cache_dir)
        for res in resources:
            nltk.download(res, download_dir=self.nltk_cache_dir)

    @property
    def nltk(self):
        if not self.nltk_downloaded:
            self._download_nltk()
            self.nltk_downloaded = True
        return nltk

    async def get_embeddings(self,
                             text,
                             model=DEFAULT_EMBEDDING_MODEL,
                             source='app'):
        if source == 'app':
            data = {
                'text': text,
                'model': model,
                'cache_dir': self.sentence_transformers_cache_dir
            }
            response = await self._send_request(endpoint='embeddings', data=data)
            if response['status'] != 'success':
                raise ValueError(f'Error in response: {response}')
            else:
                return response['data']['embeddings']

        elif source == 'local':
            model = load_embedding_model(model=model, cache_folder=self.sentence_transformers_cache_dir)
            return model.encode(text)
        else:
            raise ValueError(f'Unknown source: {source}')
