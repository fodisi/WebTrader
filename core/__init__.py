
#!/usr/bin/env python3

import os

from flask import Flask
from flask_marshmallow import Marshmallow

from .controllers.login import login_ctrl as login
from .controllers.home import home_ctrl as home
from .controllers.dashboard import dashboard_ctrl as dashboard
from .controllers.buy import buy_ctrl as buy
from .controllers.sell import sell_ctrl as sell
from .controllers.lookup import lookup_ctrl as lookup
from .controllers.quote import quote_ctrl as quote
from .controllers.order import order_ctrl as order
from .controllers.logout import logout_ctrl as logout


omnibus = Flask(__name__)
ma = Marshmallow(omnibus)

# TODO create dinamic secret_key
omnibus.secret_key = 'You Will Never Guess'


omnibus.register_blueprint(login)
omnibus.register_blueprint(home)
omnibus.register_blueprint(dashboard)
omnibus.register_blueprint(buy)
omnibus.register_blueprint(sell)
omnibus.register_blueprint(lookup)
omnibus.register_blueprint(quote)
omnibus.register_blueprint(order)
omnibus.register_blueprint(logout)
