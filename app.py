import os

from flask import Flask, redirect, render_template
from flask_restful import Api
from webargs.flaskparser import parser, abort
from flasgger import Swagger, swag_from

from models import Url
from resources.Short import ShortUrl

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3
}
swagger = Swagger(app)


@parser.error_handler
def handle_request_parsing_error(err, req, schema):
    abort(422, errors=err.messages)


@app.route('/api')
def api_reference():
    return render_template('api.html')


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


api.add_resource(ShortUrl, '/short')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
