import config
import tornado.web
import webcommon.server
import bitssignup.controllers

routes = [
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    (r"/", bitssignup.controllers.MainHandler)
]

webcommon.server.start(routes, config)
