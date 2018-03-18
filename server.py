import os

from jedi import Script
from flask import Flask, request, jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs


app = Flask(__name__)
app.debug = 'DEBUG' in os.environ


def extract_completion_data(completion, desc=False):
    """
    Convert individual completion data to jsonifiable dict
    """
    data = {
        'name': completion.name,
        'full_name': completion.full_name,
        'description': completion.description,
        'module_name': completion.module_name
    }
    if desc:
        data['full_desc'] = completion.docstring()
    return data


def get_completions(source, line, column, get_full_desc=False):
    """
    Get a list of dict of completions for the given source
    """
    source = Script(source, line+1, column+1)
    completions = source.completions()

    data = list(
        map(lambda c: extract_completion_data(c, get_full_desc), completions)
    )
    return data


@app.route('/', methods=('POST',))
@use_kwargs({
    'source': fields.Str(required=True, location='json'),
    'line': fields.Int(required=True, location='json'),
    'column': fields.Int(required=True, location='json'),
    'get_full_desc': fields.Bool(required=True, location='json', default=False)
})
def index(**kwargs):
    completions = get_completions(**kwargs)
    return jsonify(data=completions)


@app.after_request
def add_cors(response):
    """
    To allow cross originn xhr
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(debug=True)
