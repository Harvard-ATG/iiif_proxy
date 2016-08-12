import requests
import json
import logging

logger = logging.getLogger(__name__)

class ManifestProxy(object):
	url_for = {
		'lib': 'http://iiif.lib.harvard.edu',
		'huam': 'http://iiif.harvardartmuseums.org'
	}
	def __init__(self, path=''):
		self.org = path.split('/')[2]
		self.identifier = '/'.join(path.split('/')[3:])
		self.url = '%s/%s' % (self.url_for[self.org], self.identifier)
		self.res = None
		self.data = None

	def load(self):
		self.res = requests.get(self.url)
		if self.res.status_code == 200:
			self.data = self.transfrom(self.res.json())
		return self

	def transform(self, data):
		return None

	def serialize(self):
		return json.dumps(self.data, indent=2, sort_keys=True)

def application(env, start_response):
	status = '200 OK'
	headers = [('Content-Type', 'application/json')
	output = ''

	try:
		proxy = ManifestProxy(env['PATH_INFO']).load()
		if proxy.res.status_code == 200:
			status = '200 OK'
			output = proxy.serialize()
		else:
			status = '404 Not Found'
	except Exception as e:
		status = '500 Internal Server Error'
		output = json.dumps({"error": str(e)})

	start_response(status, headers)

	return output

