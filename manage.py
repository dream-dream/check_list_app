import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_check_list import app
from flask_check_list.views.view import api


app.register_blueprint(api, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
