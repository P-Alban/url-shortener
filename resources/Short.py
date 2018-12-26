from flask import request
from flask_restful import Resource
from validators import url
from webargs import fields, ValidationError
from webargs.flaskparser import use_kwargs

import utils
from models import Url


def validate_url(base_url):
    if not url(base_url):
        raise ValidationError("Invalid url")
    return True


class ShortUrl(Resource):
    args = {
        'base_url': fields.Str(required=True, validate=validate_url)
    }

    @staticmethod
    @use_kwargs(args)
    def post(base_url):
        base = request.url_root
        short_url = utils.encode(Url.add_url(base_url).id)
        return {'result': base + short_url}
