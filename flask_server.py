import os

from jedi import Script
from flask import Flask, request, jsonify, render_template
from webargs import fields
from webargs.flaskparser import use_kwargs

from autocomplete import get_completions


app = Flask(__name__)
app.debug = 'DEBUG' in os.environ


@app.route('/', methods=('POST',))
@use_kwargs({
    'source': fields.Str(required=True, location='json'),
    'line': fields.Int(required=True, location='json'),
    'column': fields.Int(required=True, location='json'),
    'get_full_desc': fields.Bool(location='json', default=False)
})
def process(**kwargs):
    completions = get_completions(**kwargs)
    return jsonify(data=completions)


@app.route('/', methods=('GET',))
def index():
    return render_template('index.html')


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    exc = getattr(err, 'exc')
    if exc:
        messages = exc.messages
    else:
        messages = ['Invalid request']
    return jsonify({
        'messages': messages,
    }), 422


@app.after_request
def add_cors(response):
    """
    To allow cross originn xhr
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
