import unittest
import json
import os.path
from proxy import ManifestProxy

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

class TestManifestProxy(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestManifestProxy, self).__init__(*args, **kwargs)
    self.manifests = {}
    self.fake_proxy_server_url = 'https://iiif.localhost'

  def setUp(self):
    fixtures = {
      'lib': ['lib_drs_15372472.json', 'lib_drs_3710791.json'],
      'huam':['huam_object_299843.json'],
    }
    for org, list_of_manifests in fixtures.iteritems():
      if org not in self.manifests:
        for filename in list_of_manifests:
          with open(os.path.join(FIXTURES_DIR, filename)) as f:
            filedata = json.loads(f.read())
            self.manifests.setdefault(org, []).append(filedata)

  def test_transform(self):
    for org, manifests in self.manifests.iteritems():
      for manifest in manifests:
        proxy = ManifestProxy(
          proxy_server_url=self.fake_proxy_server_url, 
          org=org,
          identifier='manifest/123',
        )
        result = proxy.transform(manifest)
        self.assertEqual(result['@id'], manifest['@id'])
      
        for i, canvas in enumerate(result['sequences'][0]['canvases']):
          actual_resource_url = canvas['images'][0]['resource']['@id']
          actual_service_url = canvas['images'][0]['resource']['service']['@id']
          self.assertEqual(actual_resource_url, proxy.get_image_url(actual_resource_url))
          self.assertEqual(actual_service_url, proxy.get_image_url(actual_service_url))
          print actual_service_url
  
  def test_image_proxy_url(self):
    proxy = ManifestProxy(
      proxy_server_url=self.fake_proxy_server_url, 
      org='lib',
      identifier='path/to/manifest.json',
    )
    actual_resource_url = 'http://ids.lib.harvard.edu/ids/iiif/43182083/full/full/0/native.jpg'
    expected_resource_url = '%s/images/ids/iiif/43182083/full/full/0/native.jpg' % self.fake_proxy_server_url
    actual_service_url = 'http://ids.lib.harvard.edu/ids/iiif/43182083'
    expected_service_url = '%s/images/ids/iiif/43182083' % self.fake_proxy_server_url
    
    self.assertEqual(proxy.get_image_url(actual_resource_url), expected_resource_url)
    self.assertEqual(proxy.get_image_url(actual_service_url), expected_service_url)
  
if __name__ == "__main__":
  unittest.main()
