// console screen class
function Screen(height, id) {
  Screen.prototype.write = function(line, message) {
    var lines = this.backBuffer.getElementsByTagName('div');
    lines[line].innerHTML = message;
  };

  Screen.prototype.flip = function() {
    var front = document.getElementById(this._id);
    document.body.replaceChild(this.backBuffer, front);
    this.backBuffer = this.backBuffer.cloneNode(true);
  };

  // TODO リファクタリング
  Screen.prototype.receve = function(data) {
    this._accept(data);
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
    var update = split_command(command);
    this.write(update.type, update.message);
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
