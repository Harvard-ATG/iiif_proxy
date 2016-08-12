import unittest
import json
import os.path
from proxy import ManifestProxy

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

class TestManifestProxy(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestManifestProxy, self).__init__(*args, **kwargs)
    self.manifests = {}
    self.fake_server_url = 'https://iiif.localhost'
    self.fake_proxy_server_url = '%s/images' % self.fake_server_url

  def setUp(self):
    fixtures = {
      'lib': 'lib_drs_15372472.json',
      'huam':'huam_object_299843.json'
    }
    for org, filename in fixtures.iteritems():
      if org not in self.manifests:
        with open(os.path.join(FIXTURES_DIR, filename)) as f:
          self.manifests[org] = json.loads(f.read())

  def test_transform(self):
    for org in self.manifests:
      manifest = self.manifests[org]
      path = '%s/manifest/123' % org
      proxy = ManifestProxy(self.fake_proxy_server_url, path)
      result = proxy.transform(manifest)
      self.assertEqual(result['@id'], manifest['@id'])
    
      for i, canvas in enumerate(result['sequences'][0]['canvases']):
        actual_resource_url = canvas['images'][0]['resource']['@id']
        actual_service_url = canvas['images'][0]['resource']['service']['@id']
        self.assertEqual(actual_resource_url, proxy.get_image_url(actual_resource_url))
        self.assertEqual(actual_service_url, proxy.get_image_url(actual_service_url))
  
  def test_image_proxy_url(self):
    proxy = ManifestProxy(self.fake_server_url, 'lib/path/to/manifest.json')
    actual_resource_url = 'http://ids.lib.harvard.edu/ids/iiif/43182083/full/full/0/native.jpg'
    expected_resource_url = '%s/ids/iiif/43182083/full/full/0/native.jpg' % self.fake_proxy_server_url
    actual_service_url = 'http://ids.lib.harvard.edu/ids/iiif/43182083'
    expected_service_url = '%s/ids/iiif/43182083' % self.fake_proxy_server_url
    
    self.assertEqual(proxy.get_image_url(actual_resource_url), expected_resource_url)
    self.assertEqual(proxy.get_image_url(actual_service_url), expected_service_url)
  
if __name__ == "__main__":
  unittest.main()
