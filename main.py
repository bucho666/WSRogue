# -*- coding: utf-8 -*-
from server import WebSocketServer
from handler import Handler

class Service(object):
  def enter(self, socket):
    # Handler(socket).enter()
    Handler.attach(socket)

  def leave(self, socket):
    Handler.of(socket).leave()

  def receve(self, socket, data):
    Handler.of(socket).receve(data)

if __name__ == '__main__':
  WebSocketServer(Service()).run(7003)
