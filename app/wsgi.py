import requests
import json

class ManifestLoader(object):
	org_urls = {
		'lib': 'http://iiif.lib.harvard.edu',
		'huam': 'http://iiif.harvardartmuseums.org'
	}
	def __init__(path):	
		self.path = path
		self.response = None
		self.data = None
	def get_org(self):
		return self.path.split('/')[1]
	def get_identifier(self):
		return '/'.join(self.path.split('/')[2:])
	def get_url(self):
		context = {}
		context['base_url'] = self.org_urls[self.get_org()]
		context['identifier'] = self.get_identifier()
		return '{base_url}{identifier}'.format(**context)
	def fetch(self):
		self.response = requests.get(self.get_url())
		self.data = self.response.json()
		return self
	def transform(self):
		return self
	def serialize(self):
		return json.dumps(self.data)

def application(env, start_response):
	start_response('200 OK', [('Content-Type', 'application/json')])
	#try:
	#	loader = ManifestLoader(env['PATH_INFO'])
	#	loader.fetch().transform()
	#	output = loader.serialize()
	#except Exception as e:
	#	output = str(e)
	return 'Hello world! ' + str(env)

