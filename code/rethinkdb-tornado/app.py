import os

# Get tornado
import tornado.escape
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
from tornado.concurrent import Future

# Get rethink
import rethinkdb as r

# Get jinja
from jinja2 import Environment, FileSystemLoader

template_env = Environment(loader=FileSystemLoader("templates"))


# !!! Set loop type to tornado
r.set_loop_type("tornado")

# Configure the connection
RDB_HOST = '50.116.0.34'
RDB_PORT = 28015
DB = 'CheeseTornado'


class HomeHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def prepare(self):
        self.rdb_conn = r.connect(RDB_HOST, RDB_PORT, DB)

    @tornado.gen.coroutine
    def get(self):
        conn = yield self.rdb_conn

        cheese = yield r.table('Cheese').run(conn)

        cheese_collection = []
        while(yield cheese.fetch_next()):
            if len(cheese_collection) >= 9:
                break
            c = yield cheese.next()
            cheese_collection.append(c)

        home_template = template_env.get_template("home.html")

        self.write(home_template.render(all_cheese=cheese_collection))


listeners = set()


@tornado.gen.coroutine
def show_cheese():
    while True:
        try:
            conn = yield r.connect(RDB_HOST, RDB_PORT, DB)

            cheese_feed = yield r.table("Cheese").changes().run(conn)

            while (yield cheese_feed.fetch_next()):
                new_cheese = yield cheese_feed.next()
                for listener in listeners:
                    listener.write_message(new_cheese)
        except:
            pass


class WSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):

        self.stream.set_nodelay(True)

        # Add to the user list
        listeners.add(self)

    def on_close(self):
        if self in listeners:
            listeners.remove(self)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    public_folder = os.path.join(current_dir, 'public')
    tornado_app = tornado.web.Application([
        ('/', HomeHandler),
        (r'/ws', WSocketHandler),
        (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': public_folder }),
    ],
        cookie_secret=str(os.urandom(30))
    )
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().add_callback(show_cheese)
    tornado.ioloop.IOLoop.instance().start()