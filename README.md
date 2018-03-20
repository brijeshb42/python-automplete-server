```bash
mkvirtualenv python-automplete-server
pip install -r requirements.txt
python server.py
```

Send a POST request to [https://python-autocomplete-server.herokuapp.com/](https://python-autocomplete-server.herokuapp.com/) with the following json body -

```json
{
  source: 'your python source code',
  line: 'the line in which the cursor is present (0 index)',
  column: 'the column number of the cursor(0 index)'
}
```
