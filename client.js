cscreen = new ConsoleScreen(22);

document.bgColor = 'black';
document.fgColor = 'silver';
document.body.style.fontFamily = 'Courier New';
try {
  var host = "ws://localhost:7003/";
  var s = new WebSocket(host);
  // 接続開始処理
  s.onopen = function (e) {
    cscreen.write(21, '<font color="green">connected</font>');
    cscreen.flip()
  };
  // 切断処理
  s.onclose = function (e) {
    cscreen.write(21, '<font color="red">disconnect</font>');
    cscreen.flip()
  };
  // メッセージ受信処理
  s.onmessage = function (e) {
    cscreen.receve(e.data);
  };
  // 接続エラー処理
  s.onerror = function (e) {
    cscreen.write(21, 'error');
    cscreen.flip()
  };
  // 入力処理
  document.onkeypress= function (e) {
    s.send(e.charCode)
  };
} catch (ex) {
  // 例外処理
  cscreen.write(21, 'exception');
  cscreen.flip()
}


