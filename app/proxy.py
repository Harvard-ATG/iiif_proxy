import json
import requests
import logging

logger = logging.getLogger(__name__)

class ManifestProxy(object):
	"""
	The ManifestProxy class is responsible for requesting a IIIF Manifest (JSON format)
	and replacing all references to IIIF image resources to point to a proxy server.
	
	The end goal is to configure the proxy server so that it supports SSL and can
	therefore serve up IIIF manifests and images securely. This is a requirement
	for IIIF clients (Mirador) running on secure sites (Canvas).
	"""

	image_url = {
		'lib': 'http://ids.lib.harvard.edu',
		'huam': 'http://ids.lib.harvard.edu',
	}
	
	manifest_url = {
		'lib': 'http://iiif.lib.harvard.edu',
		'huam': 'http://iiif.harvardartmuseums.org'
	}
	
	image_proxy_fmt = '{base_url}/images/{identifier}'

	def __init__(self, proxy_server_url, request_path):
		path = request_path.split('/')
		if len(path) < 2:
			raise Exception("invalid request path (length < 2). expected: {org}/path/to/manifest")
		self.org = path[0]
		if self.org not in self.manifest_url or self.org not in self.image_url:
			raise Exception("invalid org: %s" % self.org)
		self.identifier = '/'.join(path[1:])
		self.proxy_server_url = proxy_server_url 
		self.res = None
		self.data = None
		logger.debug("instantiated manifest proxy with org [%s] manifest identifier [%s]" %(self.org, self.identifier))

	def load(self):
		url = '%s/%s' % (self.manifest_url[self.org], self.identifier)
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
						resource['@id'] = self.get_image_url(resource['@id'])
					if '@id' in service:
						service['@id'] = self.get_image_url(service['@id'])
		return manifest

	def get_image_url(self, url):
		if url.startswith(self.image_url[self.org]):
			url_path = url.replace(self.image_url[self.org], '', 1)
			return self.image_proxy_fmt.format(base_url=self.proxy_server_url, identifier=url_path[1:])
		return url

	def serialize(self):
		return json.dumps(self.data, indent=2, sort_keys=True)

