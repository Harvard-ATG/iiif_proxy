import json
import logging
from proxy import ManifestProxy

logger = logging.getLogger(__name__)

def get_proxy_server_url(env):
	host_port_specified = ':' in env['HTTP_HOST']
	proxy_server_url = "%s://%s" % (env['wsgi.url_scheme'], env['HTTP_HOST'])
	if not host_port_specified and env['SERVER_PORT'] not in ('80', '443'):
		proxy_server_url = '%s:%s' % (proxy_server_url, env['SERVER_PORT'])
	return proxy_server_url

def application(env, start_response):
	logging.basicConfig(level=logging.DEBUG)
	ch = logging.StreamHandler(env['wsgi.errors'])
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
	logger.addHandler(ch)

	status = '200 OK'
	headers = [('Content-Type', 'application/json')]
	output = ''

	logger.debug(env)
	logger.info("handling request with path=%s" % env['PATH_INFO'])
	try:
		path = env['PATH_INFO'].split('/')[2:]
		proxy = ManifestProxy(
			proxy_server_url=get_proxy_server_url(env),
			org=path[0],
			identifier='/'.join(path[1:]),
		).load()
		if proxy.res.status_code == 200:
			status = '200 OK'
			output = proxy.serialize()
		else:
			status = '404 Not Found'
	except Exception as e:
		status = '500 Internal Server Error'
		output = json.dumps({"error": str(e)})
		logger.error(str(e))

	logger.info("starting response with status=%s" % status)
	start_response(status, headers)

	return output
