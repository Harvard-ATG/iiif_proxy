## Quickstart

```sh
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo ln -s /vagrant/etc/nginx/nginx.conf /etc/nginx/sites-enabled/iiif_proxy
$ sudo service nginx stop
$ sudo service nginx start
$ sudo cp /vagrant/etc/init/app.conf /etc/init/iiif_proxy.conf
$ sudo service iiif_proxy start
```

### Examples

##### IIIF Image URL

- Image URL: http://ids.lib.harvard.edu/ids/iiif/15372852/full/400,/0/native
- Proxy URL: http://localhost:8080/images/ids/iiif/15372852/full/400,/0/native

#####Library Manifest

- Manifest URL: http://iiif.lib.harvard.edu/manifests/drs:15372472
- Proxy URL: http://localhost:8080/meta/lib/manifests/drs:15372472

#####Harvard Art Museum Manifes

- Manifest URL: http://iiif.harvardartmuseums.org/manifests/object/299843
- Proxy URL: http://localhost:8080/meta/huam/manifests/object/299843

