import config
import tornado.web
import webcommon.server
import bitssignup.controllers
import os

root_dir = os.path.dirname(os.path.realpath(__file__))
routes = [
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(root_dir, "static")}),
    (r"/", bitssignup.controllers.MainHandler)
]

webcommon.server.start(routes, config)
