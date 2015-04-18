# -*- coding: utf-8 -*-
from server import WebSocketServer
from screen import Screen

class Service(object):
  def __init__(self):
    self._x, self._y = (0, 0)
    self._screen = Screen((80, 21))

  def enter(self, socket):
    self._screen = Screen((80, 21))
    self._screen.flush(socket)

  def leave(self, socket):
    pass

  def receve(self, socket, data):
    self._screen.fill('.')
    key = chr(int(data))
    if key == 'l': self._x += 1
    if key == 'h': self._x -= 1
    if key == 'j': self._y += 1
    if key == 'k': self._y -= 1
    self._screen.put('@', (self._x, self._y), 'olive')
    self._screen.write(u'入力キー:%s' % key, (4, 20), 'lime')
    self._screen.flush(socket)

if __name__ == '__main__':
  WebSocketServer(Service()).run(7003)
