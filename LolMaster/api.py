from LolMaster.error import KeyNotValidError, NotReachableError
from LolMaster import config
from typing import Iterable, Union, Dict
import requests
import logging
import time


class RiotURL:
	def __init__(self, url):
		self.url = url

	@staticmethod
	def absolute_url(url: str) -> str:
		region = config.get_region()
		base = "https://%s.api.riotgames.com" % region
		return base + url

	def add_query(self, query_name: str, queries: Union[str, Iterable[str]]) -> 'RiotURL':
		if type(queries) == str:
			queries = [queries]
		for query in queries:
			if '?' in self.url:
				self.url += '&'
			else:
				self.url += '?'
			self.url += '%s=%s' % (query_name, query)
		return self

	def request(self, max_retry: int = 5) -> Union[None, Dict]:
		if self.url[0] == '/':
			self.url = RiotURL.absolute_url(self.url)
		self.add_query('api_key', config.get_key())

		while max_retry > 0:
			r = requests.get(self.url)

			if r.status_code == 200:
				return r.json()
			elif r.status_code == 404:
				logging.warning("Data not found: %s" % self.url)
				return None
			elif r.status_code == 429:
				backoff = r.headers.get('Retry-After')
				if backoff is None:
					logging.warning("Code 429 with no Retry-After.")
					logging.warning(r.headers)
					backoff = 30
				backoff = int(backoff)
				logging.info("Backoff for %d seconds." % backoff)
				time.sleep(backoff)
				continue
			else:
				logging.error(self.url)
				logging.error(r.json().get('status'))

				if r.status_code == 401:
					logging.error("API token is not included.")
					raise NotReachableError
				elif r.status_code == 403:
					logging.error("API token or URL is not valid.")
					raise KeyNotValidError
				else:
					logging.error("Unknown error of code %d. Retrying." % r.status_code)
					max_retry -= 1
					continue

		return None
