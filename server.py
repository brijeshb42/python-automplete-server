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
    'get_full_desc': fields.Bool(location='json', default=False)
})
def process(**kwargs):
    completions = get_completions(**kwargs)
    return jsonify(data=completions)


@app.route('/', methods=('GET',))
def index():
    return """
    <h4>Send a POST request with the following JSON body</h4>
    <p>
<pre>
{
    "source": "The python source code to process",
    "line": 0 (the line in which the cursor is present, 0 indexed),
    "column": 0 (the column of the line of cursor, 0 indexed)
}
</pre>
    </p>
    """


@app.errorhandler(422)
def handle_unprocessable_entity(err):
    # webargs attaches additional metadata to the `data` attribute
    exc = getattr(err, 'exc')
    if exc:
        # Get validations from the ValidationError object
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


if __name__ == '__main__':
    app.run(debug=True)
