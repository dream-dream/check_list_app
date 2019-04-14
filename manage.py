import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_script import Manager, Server  # use that design your own command through function or class method

from .__init__ import app
from .views.view import api

manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
                    )

app.register_blueprint(api, url_prefix='/api/v1')

if __name__ == '__main__':
    manager.run()
