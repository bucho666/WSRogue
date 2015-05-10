# -*- coding: utf-8 -*-
from screen import Screen
from game import Character
from game import MapFile
from game import View

class Handler(object):
  _handlers = dict()
  _map = MapFile.load(open('map.dat', 'r'))

  @classmethod
  def of(cls, socket):
    return cls._handlers[socket]

  @classmethod
  def render_all(cls):
    for handler in cls._handlers.values():
      handler.render()

  @classmethod
  def attach(cls, socket):
    InputNameHandler(socket).enter()

  def __init__(self):
    self._messages = Messages()

  def enter(self):
    pass

  def leave(self):
    pass

  def receve(self, data):
    header, command = data.split(':', 1)
    if header == 'k':
      self.receve_key(chr(int(command)))
    else:
      self.receve_command(command)
    self.render_all()

  def render(self):
    pass

  def receve_key(self, key):
    pass

  def receve_command(self, command):
    pass

  def send_message(self, message):
    self._messages.add(message)

class GameHandler(Handler):
  def __init__(self, socket, character):
    Handler.__init__(self)
    self._socket = socket
    self._screen = Screen((32, 12))
    self._character = character
    self._view = View(character, self._map)

  def enter(self):
    name = self._character.name()
    self.send_message_all('"%s"がログインしました。' % name)
    self.send_message('ようこそ %s。' % name)
    self._handlers[self._socket] = self
    self._map.put_character(self._character, self._map.random_open_coordinate())
    self.render_all()

  def leave(self):
    del self._handlers[self._socket]
    self._map.remove_character(self._character)
    self.render_all()

  def receve_key(self, key):
    if key == 'l': self._map.move_character(self._character, ( 1,  0))
    if key == 'h': self._map.move_character(self._character, (-1,  0))
    if key == 'j': self._map.move_character(self._character, ( 0,  1))
    if key == 'k': self._map.move_character(self._character, ( 0, -1))

  def receve_command(self, command):
    message = '%s: %s' % (self._character.name(), command)
    self.send_message_all(message)

  def send_message_all(self, message):
    for handler in self._handlers.values():
      if isinstance(handler, GameHandler):
        handler.send_message(message)

  def render(self):
    self._view.render(self._screen)
    self._screen.flush(self._socket)
    self._messages.flush(self._socket)

class InputNameHandler(Handler):
  def __init__(self, socket):
    Handler.__init__(self)
    self._socket = socket
    self._character = Character('@', 'olive')

  def enter(self):
    self._handlers[self._socket] = self
    self.send_message('<font color="yellow">名前を入力してください。</font>')
    self.render()

  def receve_key(self, key):
    pass

  def receve_command(self, command):
    c = Character('@', 'olive', command)
    GameHandler(self._socket, c).enter()

  def render(self):
    self._messages.flush(self._socket)

class Messages(object):
  def __init__(self):
    self._messages = []

  def add(self, message):
    self._messages.append(message)

  def flush(self, socket):
    for message in self._messages:
      socket.send('messageScreen:%s' % message)
    self._messages = []
