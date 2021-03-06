from jedi import Script

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
