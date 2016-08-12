import json
import logging
from proxy import ManifestProxy

logger = logging.getLogger(__name__)

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
		base_url = "%s://%s" % (env['wsgi.url_scheme'], env['HTTP_HOST'])
		if env['SERVER_PORT'] != '80':
			base_url = '%s:%s' % (base_url, env['SERVER_PORT'])
		proxy = ManifestProxy(base_url, env['PATH_INFO'])
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
