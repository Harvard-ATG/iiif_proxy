import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

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
		logger.debug("instantiated proxy with org=%s identifier=% url=%s" % (self.org, self.identifier, self.url))

	def load(self):
		self.res = requests.get(self.url)
		logger.info("loaded url=%s response status=%s" % (self.url, self.res.status_code))
		if self.res.status_code == 200:
			self.data = self.transfrom(self.res.json())
		return self

	def transform(self, data):
		return data

	def serialize(self):
		return json.dumps(self.data, indent=2, sort_keys=True)

def application(env, start_response):
	status = '200 OK'
	headers = [('Content-Type', 'application/json')
	output = ''

	logger.info("handling request with path=%s" % env['PATH_INFO'])
	try:
		proxy = ManifestProxy(env['PATH_INFO'], logger=logger).load()
		if proxy.res.status_code == 200:
			status = '200 OK'
			output = proxy.serialize()
		else:
			status = '404 Not Found'
	except Exception as e:
		status = '500 Internal Server Error'
		output = json.dumps({"error": str(e)})

	logger.info("starting response with status=%s" % status)
	start_response(status, headers)

	return output

