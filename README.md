## Setup

Run `vagrant up` to stand up a local development environment then follow the instructions below.

#### Configure nginx server

```sh
$ sudo rm /etc/nginx/sites-enabled/default
$ sudo ln -s /vagrant/etc/nginx/iiif_proxy.conf /etc/nginx/sites-enabled/iiif_proxy
$ sudo service nginx start
```

Note: be sure to configure SSL for nginx after the basic setup is done.

#### Configure wsgi app server
[Upstart](http://upstart.ubuntu.com/) is the init system for ubuntu-like systems. 

```sh
$ sudo cp /vagrant/etc/init/iiif_proxy.conf /etc/init/iiif_proxy.conf
$ sudo service iiif_proxy start
```

See the configuration for the [uwsgi](http://uwsgi-docs.readthedocs.io/) application server in `app/config.ini`. To manually start the application server, just run `cd app && uwsgi config.ini`.

#### Monitor log files

```sh
$ sudo tail -f /var/log/nginx/error.log
$ sudo tail -f /var/log/upstart/iiif_proxy.log 
```

#### Run Unit Tests

```sh
$ nosetests app/tests
```

### URL Scheme

**IIIF Manifests**

|Pattern|Organization|URL|
|-------|------------|---|
|`/meta/lib/<identifier>`|Harvard Library|`http://iiif.lib.harvard.edu/<identifier>`|
|`/meta/huam/<identifier>`|Harvard Art Museums|`http://iiif.harvardartmuseums.org/<identifier>`|

**IIIF Images**

|Pattern|URL|
|-------|---|
|`/images/<identifier>`|`http://ids.lib.harvard.edu/<identifier>`|

_Images for the library and museum are served from the same repository._


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

