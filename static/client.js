var node = document.getElementById("editor");

let xhr = null;

CodeMirror.registerHelper('hint', 'magic', function(editor, opt, o) {
  var cursor = editor.getCursor();
  var source = editor.getValue();
  var inflight = editor.state.inflight;
  
  if (inflight) {
    return;
  }

  editor.state.inflight = true;

  const req = getCompletions(source, cursor.line, cursor.ch);
  req.then(data => {
    editor.showHint(data.data.map(item => {
      item.title = item.name;
      return item;
    }));
    editor.state.inflight = false;
  }).catch(() => {
    editor.state.inflight = false;
  });
});

CodeMirror.commands.autocomplete = function(editor) {
  CodeMirror.showHint(editor, CodeMirror.hint.magic);
};

CodeMirror.commands.fontSizePlus = function(editor) {
  const { wrapper } = editor.display;

  let fontSize = editor.getOption('fontSize') || 14;
  fontSize++;

  wrapper.style.fontSize = `${fontSize}px`;
  editor.setOption('fontSize', fontSize);
};


function getCompletions(source, line, column) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.responseType = 'json';

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          resolve(xhr.response);
        } else {
          reject();
        }
      }
    };

    xhr.open('POST', '/');
    xhr.setRequestHeader('Content-Type', 'application/json;charset=utf-8');
    xhr.send(JSON.stringify({
      source,
      line,
      column: column - 1
    }));
  });
}


var myCodeMirror = CodeMirror(node, {
  value: 'def hello():\n  pass\n',
  lineNumbers: true,
  mode: 'python',
  tabSize: 2,
  theme: 'dracula',
  lineWrapping: true,
  extraKeys: {
    'Ctrl-Space': 'autocomplete',
    'Ctrl-Plus': 'fontSizePlus'
  },
  fontSize: 16
});


window.editor = myCodeMirror;
