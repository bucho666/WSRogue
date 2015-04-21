var splitHeader = function(command) {
  var match, type, message;
  match = command.match(/^(\w+):(.*)/);
  return {
    type   : match[1],
    message: match[2]
  };
}

var Client = function () {
  document.bgColor = 'black';
  document.fgColor = 'silver';
  document.body.style.fontFamily = 'Courier New';
  try {
    var host = "ws://localhost:7003/";
    var s = new WebSocket(host);
    s.messageScreen = new MessageScreen(4, 'message_screen');
    s.mapScreen = new MapScreen(12, 'map_screen');
    // 接続開始処理
    s.onopen = function (e) {
      this.messageScreen.add('<font color="green">connected</font>');
    };
    // 切断処理
    s.onclose = function (e) {
      this.messageScreen.add('<font color="red">disconnected</font>');
    };
    // メッセージ受信処理
    s.onmessage = function (e) {
      var commands, i, length, line, command;
      commands = e.data.split('\x00');
      length = commands.length;
      for (i = 0; i < length; i++) {
        command = splitHeader(commands[i]);
        this[command.type].receve(command.message);
      }
      this.mapScreen.flip();
    };
    // 接続エラー処理
    s.onerror = function (e) {
      messageScreen.add('error');
    };
    // 入力処理
    document.onkeypress= function (e) {
      s.send(e.charCode)
    };
  } catch (ex) {
    // 例外処理
    messageScreen.add('exception');
  }
}

var client = Client();
