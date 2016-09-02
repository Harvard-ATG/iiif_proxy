import re
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
	for IIIF clients like Mirador running on secure sites like Canvas.
	"""

	# Maps an organization to their respective IIIF presentation API's for loading manifests
	manifest_url = {
		'lib': 'http://iiif.lib.harvard.edu',
		'huam': 'http://iiif.harvardartmuseums.org'
	}

	# Original URL for images expected to be found in maniefsts
	image_url_pattern = r'https?://ids.lib.harvard.edu'
	image_url_replacement = r''
	
	# Proxy URL for images 
	image_proxy_fmt = '{url}/images/{identifier}'

	def __init__(self, **kwargs): 
		self.proxy_server_url = kwargs.pop('proxy_server_url', None)
		self.org = kwargs.pop('org', None)
		self.identifier = kwargs.pop('identifier', None)
		if kwargs:
			raise TypeError('Unexpected **kwargs: %r' % kwargs)
		if self.org is None or self.org not in self.manifest_url:
			raise ValueError("invalid org: %s" % self.org)
		if self.identifier is None:
			raise ValueError("invalid identifier: %s" % self.identifier)
		if self.proxy_server_url is None:
			raise ValueError("invalid proxy server url: %s" % self.proxy_server_url)
		self.res = None
		self.data = None
		logger.debug("instantiated manifest proxy with url [%s] org [%s] manifest identifier [%s]" %(self.proxy_server_url, self.org, self.identifier))

	def load(self):
		'''
		Loads the requested IIIF manifest (i.e. JSON file).
		If the request is successful, modify the manifest so that image URLs are proxied.
		'''
		url = '%s/%s' % (self.manifest_url[self.org], self.identifier)
		self.res = requests.get(url)
		if self.res.status_code == 200:
			self.data = self.transform(self.res.json())
		return self

	def transform(self, manifest):
		'''
		Modifies the given IIIF manifest so that all IIIF image server URLs are proxied.
		'''
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
		'''
		Returns the proxy URL for a given IIIF image server URL
		'''
		if re.match(self.image_url_pattern, url):
			url_path = re.sub(self.image_url_pattern, self.image_url_replacement, url)
			return self.image_proxy_fmt.format(url=self.proxy_server_url, identifier=url_path[1:])
		return url

	def serialize(self):
		return json.dumps(self.data, indent=2, sort_keys=True)

