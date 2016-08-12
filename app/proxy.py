import json
import requests
import logging

logger = logging.getLogger(__name__)

class ManifestProxy(object):
	image_url = 'http://ids.lib.harvard.edu'
	manifest_url = {
		'lib': 'http://iiif.lib.harvard.edu',
		'huam': 'http://iiif.harvardartmuseums.org'
	}
	def __init__(self, base_url, request_path):
		path = request_path.split('/')
		if len(path) < 4:
			raise Exception("invalid request path (length < 4). expected: /{prefix}/{org}/{identifier}...")
		self.org = path[2]
		self.identifier = '/'.join(path[3:])
		self.base_url = base_url
		self.res = None
		self.data = None
		logger.debug("instantiated manifest proxy with %s %s" %(self.org, self.identifier))

	def load(self):
		url = '%s/%s' % (self.manifest_url.get(self.org, ''), self.identifier)
		self.res = requests.get(url)
		if self.res.status_code == 200:
			self.data = self.transform(self.res.json())
		return self

	def transform(self, manifest):
		sequences = manifest.get('sequences', [])
		for sequence in sequences:
			canvases = sequence.get('canvases', [])
			for canvas in canvases:
				images = canvas.get('images', [])
				for image in images:
					resource = image.get('resource', {})
					service = resource.get('service', {})
					if '@id' in resource:
						resource['@id'] = self.image_proxy_url(resource['@id'])
					if '@id' in service:
						service['@id'] = self.image_proxy_url(service['@id'])
		return manifest

	def image_proxy_url(self, url):
		if url.startswith(self.image_url):
			url_path = url.replace(self.image_url, '', 1)
			return "%s/images/%s" % (self.base_url, url_path[1:])
		return url

	def serialize(self):
		return json.dumps(self.data, indent=2, sort_keys=True)

