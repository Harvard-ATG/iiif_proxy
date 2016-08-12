import json
import logging
from proxy import ManifestProxy

logger = logging.getLogger(__name__)

def get_proxy_server_url(env):
	proxy_server_url = "%s://%s" % (env['wsgi.url_scheme'], env['HTTP_HOST'])
	if env['SERVER_PORT'] != '80':
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

	logger.info("handling request with path=%s" % env['PATH_INFO'])
	try:
		proxy_server_url = get_proxy_server_url(env)
		request_path = env['PATH_INFO'].split('/')
		proxy = ManifestProxy(proxy_server_url, '/'.join(request_path[2:]))
		proxy.load()
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
