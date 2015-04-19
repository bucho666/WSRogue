# -*- coding: utf-8 -*-
from screen import Screen

class Map(object):
  def __init__(self):
    self._character = dict()

  def render(self, screen):
    screen.fill('.')

  def put_character(self, character, pos):
    self._character[pos] = character

  def move_character(self, character, direction):
    pass

class Character(object):
  def __init__(self, glyph, color):
    self._glyph = glyph
    self._color = color

  def render(self, screen, coordinate):
    screen.put(self._glyph, coordinate, self._color)

class Handler(object):
  _handlers = dict()
  _map = Map()

  @classmethod
  def of(cls, socket):
    return cls._handlers[socket]

  def __init__(self, socket):
    self._character = Character('@', 'olive')
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
    key = chr(int(data))
    if key == 'l': self._x += 1
    if key == 'h': self._x -= 1
    if key == 'j': self._y += 1
    if key == 'k': self._y -= 1
    self._map.render(self._screen)
    self._character.render(self._screen, (self._x, self._y))
    self._screen.flush(self._socket)
