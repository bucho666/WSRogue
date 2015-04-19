// console screen class
function Screen(height, id) {
  Screen.prototype.write = function(line, message) {
    lines = this.backBuffer.getElementsByTagName('div');
    lines[line].innerHTML = message;
  };

  Screen.prototype.flip = function() {
    var front = document.getElementById(this._id);
    document.body.replaceChild(this.backBuffer, front);
    this.backBuffer = this.backBuffer.cloneNode(true);
  };

  Screen.prototype.receve = function(data) {
    var commands, i, length;
    commands = data.split('\x00');
    length = commands.length;
    for (i=0;i < length; i++) {
      this._accept(commands[i]);
    }
    this.flip();
  }

  Screen.prototype._create_div = function(text) {
    var div = document.createElement('div');
    div.innerHTML = text;
    return div;
  }

  var screen = document.createElement('div');
  this._id = id;
  screen.id = this._id;
  document.body.appendChild(screen);
  for (var i = 0; i < height; i++) {
    screen.appendChild(this._create_div('<br>'));
  }
  this.backBuffer = screen.cloneNode(true);
}

function MapScreen(height, id) {
  var that = new Screen(height, id);

  that._accept = function(command) {
    var match, line, message;
    match = command.match(/^(\d+):(.*)/);
    line = match[1];
    message = match[2];
    this.write(line, message);
  }

  return that;
}

function MessageScreen(height, id) {
  var that = new Screen(height, id);

  that.add = function(message) {
    this.backBuffer.removeChild(this.backBuffer.firstChild);
    this.backBuffer.appendChild(this._create_div(message));
    this.flip();
  }

  return that;
}
