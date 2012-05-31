import bottle
bottle.debug(True)
bottle.reloader=True
from bin import todo

title=body=auth=''

BASE_URL = "http://localhost:8080/"
STATIC_ROOT_PATH = "static/"

@bottle.route('/static/<filename:path>')
def static_file(filename='index.html'):
    return bottle.static_file(filename, root='static')


class StripPathMiddleware(object):
  def __init__(self, app):
    self.app = bottle.app
  def __call__(self, e, h):
    e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
    return self.app(e,h)


@bottle.route('/')
@bottle.view('gui/one.tpl')
def lobby():
    title = 'Welcome'
    body = 'Welcome to Python '
    return dict(title=title, body=body)

@bottle.error(404)
@bottle.view('gui/error.tpl')
def error404(error):
    title = 'Error 404: Not Found'
    error = 'Sorry, the requested URL caused an error' # @todo find url request.???
    return dict(title=title, error=error, auth=auth)

@bottle.error(500)
@bottle.view('gui/error.tpl')
def error500(error):
    title = 'Error 500: Internal Server Error'
    error = "The server encountered something unexpected that didn't allow it to complete the request."
    return dict(title=title, error=error, auth=auth)

app = StripPathMiddleware(bottle.app)

if __name__ == "__main__":
  bottle.debug(True)

bottle.run(host='localhost', port=8080)
