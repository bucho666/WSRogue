// console screen class
function ConsoleScreen(height) {
  var screen = document.createElement('div');
  screen.id = 'screen'
  document.body.appendChild(screen);
  for (var i = 0; i < height; i++) {
    var line = document.createElement('div');
    line.innerHTML = '<br>';
    screen.appendChild(line);
  }
  this.backBuffer = screen.cloneNode(true);

  this.write = function(line, message) {
    lines = this.backBuffer.getElementsByTagName('div');
    lines[line].innerHTML = message;
  };

  this.flip = function() {
    var front = document.getElementById('screen');
    document.body.replaceChild(this.backBuffer, front);
    this.backBuffer = this.backBuffer.cloneNode(true);
  };

  this.receve = function(data) {
    var commands, i, length;
    commands = data.split('\x00');
    length = commands.length;
    for (i=0;i < length; i++) {
      this._accept(commands[i]);
    }
  }

  this._accept = function(command) {
    if (command === 'flip') {
      this.flip();
    } else {
      this._update_line(command);
    }
  }

  this._update_line = function(command) {
    var match, line, message;
    match = command.match(/^(\d+):(.*)/);
    line = match[1];
    message = match[2];
    this.write(line, message);
  }
}
