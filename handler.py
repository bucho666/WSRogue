# -*- coding: utf-8 -*-
from screen import Screen
from game import Map
from game import Character

class Messages(object):
  def __init__(self):
    self._messages = []

  def add(self, message):
    self._messages.append(message)

  def flush(self, socket):
    for message in self._messages:
      socket.send('messageScreen:%s' % message)
    self._messages = []

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
    self._messages = Messages()
    self._character = Character('@', 'olive')
    self._map.put_character(self._character, self._map.random_open_coordinate())

  def enter(self):
    self._handlers[self._socket] = self
    self.render_all()

  def leave(self):
    del self._handlers[self._socket]

  def receve(self, data):
    header, command = data.split(':', 1)
    if header == 'k':
      self.receve_key(chr(int(command)))
    else:
      self.receve_command(command)
    self.render_all()

  def receve_key(self, key):
    if key == 'l': self._map.move_character(self._character, ( 1,  0))
    if key == 'h': self._map.move_character(self._character, (-1,  0))
    if key == 'j': self._map.move_character(self._character, ( 0,  1))
    if key == 'k': self._map.move_character(self._character, ( 0, -1))

  def receve_command(self, command):
    for handler in self._handlers.values():
      handler.send_message(command)

  def send_message(self, message):
    self._messages.add(message)

  def render(self):
    self._map.render(self._screen)
    self._screen.flush(self._socket)
    self._messages.flush(self._socket)
