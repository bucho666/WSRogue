"use strict";

// console screen class
function Screen(height, id) {
  var screen = document.createElement('div');
  this._id = id;
  screen.id = this._id;
  document.body.appendChild(screen);
  for (var i = 0; i < height; i++) {
    screen.appendChild(this._create_div('<br>'));
  }
  this.backBuffer = screen.cloneNode(true);
}

Screen.prototype.write = function(line, message) {
  var lines = this.backBuffer.getElementsByTagName('div');
  lines[line].innerHTML = message;
};

Screen.prototype.flip = function() {
  var front = document.getElementById(this._id);
  document.body.replaceChild(this.backBuffer, front);
  this.backBuffer = this.backBuffer.cloneNode(true);
};

Screen.prototype._create_div = function(text) {
  var div = document.createElement('div');
  div.innerHTML = text;
  return div;
}

function MapScreen(height, id) {
  var that = new Screen(height, id);

  that.receve = function(command) {
    var update = splitHeader(command);
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

  that.receve = that.add;

  return that;
}
