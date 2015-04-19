var messages = new MessageScreen(4, 'message_screen');
var cscreen = new MapScreen(12, 'map_screen');

document.bgColor = 'black';
document.fgColor = 'silver';
document.body.style.fontFamily = 'Courier New';
try {
  var host = "ws://localhost:7003/";
  var s = new WebSocket(host);
  // 接続開始処理
  s.onopen = function (e) {
    messages.add('<font color="green">connected</font>');
  };
  // 切断処理
  s.onclose = function (e) {
    messages.add('<font color="red">disconnected</font>');
  };
  // メッセージ受信処理
  s.onmessage = function (e) {
    cscreen.receve(e.data);
    messages.add('test:' + e.data);
  };
  // 接続エラー処理
  s.onerror = function (e) {
    message.add('error');
  };
  // 入力処理
  document.onkeypress= function (e) {
    s.send(e.charCode)
  };
} catch (ex) {
  // 例外処理
  message.add('exception');
}


