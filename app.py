import os

from flask import Flask, redirect, render_template, Request
from flask_restful import Api
from webargs.flaskparser import parser, abort

from models import Url
from resources.Short import ShortUrl


class ProxyRequest(Request):
    def __init__(self, environ, populate_request=True, shallow=False):
        super(Request, self).__init__(environ, populate_request, shallow)
        # Support SSL termination. Mutate the host_url within Flask to use https://
        # if the SSL was terminated.
        x_forwarded_proto = self.headers.get('X-Forwarded-Proto')
        if x_forwarded_proto == 'https':
            self.url = self.url.replace('http://', 'https://')
            self.host_url = self.host_url.replace('http://', 'https://')
            self.base_url = self.base_url.replace('http://', 'https://')
            self.url_root = self.url_root.replace('http://', 'https://')


@parser.error_handler
def handle_request_parsing_error(err, req, schema):
    abort(422, errors=err.messages)


@app.route('/<short>')
def do_redirect(short):
    url = Url.get_base_by_short(short)
    if url:
        return redirect(url.base_url, code=302)
    abort(404)


@app.errorhandler(404)
def return_404(error):
    return render_template('404_error.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


app = Flask(__name__)
api = Api(app)
app.request_class = ProxyRequest

api.add_resource(ShortUrl, '/short')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
