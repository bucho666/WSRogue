# -*- coding: utf-8 -*-
from screen import Screen

class Handler(object):
  _handlers = dict()

  @classmethod
  def of(cls, socket):
    return cls._handlers[socket]

  def __init__(self, socket):
    self._socket = socket
    self._x, self._y = (0, 0)
    self._screen = Screen((80, 21))

  def enter(self):
    self._screen = Screen((80, 21))
    self._screen.flush(self._socket)
    self._handlers[self._socket] = self

  def leave(self):
    del self._handlers[self._socket]

  def receve(self, data):
    self._screen.fill('.')
    key = chr(int(data))
    if key == 'l': self._x += 1
    if key == 'h': self._x -= 1
    if key == 'j': self._y += 1
    if key == 'k': self._y -= 1
    self._screen.put('@', (self._x, self._y), 'olive')
    self._screen.flush(self._socket)
