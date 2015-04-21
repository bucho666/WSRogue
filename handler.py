# -*- coding: utf-8 -*-
from screen import Screen
from game import Map
from game import Character

class Handler(object):
  _handlers = dict()
  _map = Map()

  @classmethod
  def of(cls, socket):
    return cls._handlers[socket]

  @classmethod
  def render_all(cls):
    for handler in cls._handlers.values():
      handler.render()

  def __init__(self, socket):
    self._socket = socket
    self._screen = Screen((32, 12))
    self._character = Character('@', 'olive')
    self._map.put_character(self._character, self._map.random_open_coordinate())

  def enter(self):
    self._screen.flush(self._socket)
    self._handlers[self._socket] = self
    self.render_all()

  def leave(self):
    del self._handlers[self._socket]

  def receve(self, data):
    key = chr(int(data))
    if key == 'l': self._map.move_character(self._character, ( 1,  0))
    if key == 'h': self._map.move_character(self._character, (-1,  0))
    if key == 'j': self._map.move_character(self._character, ( 0,  1))
    if key == 'k': self._map.move_character(self._character, ( 0, -1))
    # TODO DEBUG
    pos = self._map.coordinate_of_character(self._character)
    self._socket.send('messageScreen:%s' % str(pos))
    # TODO DEBUG
    self.render_all()

  def render(self):
    self._map.render(self._screen)
    self._screen.flush(self._socket)
