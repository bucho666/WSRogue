# -*- coding: utf-8 -*-
from screen import Screen

class Map(object):
  def __init__(self):
    self._character = dict()

  def render(self, screen):
    screen.fill('.')
    for coord, character in self._character.items():
      character.render(screen, coord)

  def put_character(self, character, pos):
    self._character[pos] = character

  def move_character(self, character, direction):
    (x, y) = self.coordinate_of_character(character)
    (dx, dy) = direction
    del self._character[(x, y)]
    self._character[(x + dx, y + dy)] = character

  def coordinate_of_character(self, target):
    for coord, character in self._character.items():
      if target == character: return coord
    return None

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

  @classmethod
  def render_all(cls):
    for handler in cls._handlers.values():
      handler.render()

  def __init__(self, socket):
    self._character = Character('@', 'olive')
    self._socket = socket
    self._map.put_character(self._character, (0, 0))
    self._screen = Screen((80, 21))

  def enter(self):
    self._screen = Screen((80, 21))
    self._screen.flush(self._socket)
    self._handlers[self._socket] = self

  def leave(self):
    del self._handlers[self._socket]

  def receve(self, data):
    key = chr(int(data))
    if key == 'l': self._map.move_character(self._character, ( 1,  0))
    if key == 'h': self._map.move_character(self._character, (-1,  0))
    if key == 'j': self._map.move_character(self._character, ( 0,  1))
    if key == 'k': self._map.move_character(self._character, ( 0, -1))
    self.render_all()

  def render(self):
    self._map.render(self._screen)
    self._screen.flush(self._socket)
