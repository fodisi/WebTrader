
#!/usr/bin/env python3

import os

from flask import Flask

from core.controllers.login import login_ctrl as login
from core.controllers.dashboard import dashboard_ctrl as dashboard
from core.controllers.buy import buy_ctrl as buy
from core.controllers.sell import sell_ctrl as sell
from core.controllers.lookup import lookup_ctrl as lookup
from core.controllers.quote import quote_ctrl as quote
from core.controllers.order import order_ctrl as order
from core.controllers.logout import logout_ctrl as logout


omnibus = Flask(__name__)

# TODO create dinamic secret_key
omnibus.secret_key = 'You Will Never Guess'


omnibus.register_blueprint(login)
omnibus.register_blueprint(dashboard)
omnibus.register_blueprint(buy)
omnibus.register_blueprint(sell)
omnibus.register_blueprint(lookup)
omnibus.register_blueprint(quote)
omnibus.register_blueprint(order)
omnibus.register_blueprint(logout)
