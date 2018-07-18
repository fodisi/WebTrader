
/
- Change __init__.py to generate random session key

- restructure directory to best practices. see https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

################################### CORE ###################################

####### .CORE ########
/Core

####### TEMPLATES ########
/templates
- use JINJA inheritance with blocks

templates/lookup
OK - reafactor template to use list of objects / JSON

####### CONTROLLERS ########

- Refactor non-REST functions to use JSON objects as a result

- Include HTTP codes in all API-REST functions.

- CONVERT CONTROLLERS TO CLASSES and rename file names to identify as controller
    - Dashboard
    - lookup
    - order
    - quote
    - sell
    - Dashboard
    - holding

/controllers
- IMPLEMENT REST API
    OK - Quote
    OK - Asset
    - Buy
    - Sell
    OK - Order
    - Dashboard

- Implement ADMIN controllers
    - add user
    - delete user
    - update user
    - list users
    - list users ranking dashboard

/controller/quote
- Check problem that's happening when input BTC, ETH. Apparently they are known to MarkitOneDemmand, but do not return 
    standard error message neither return a valid result.

####### MODEL ########

ALL Models
- Refactor MODELS to be totally object-oriented, with inheritance and composition, plus refactor methods to user classes attributes.


/model/quote
OK - remove __str__ method.
OK - REFACTOR MODEL AND CONTROLLER TO USET ASSET CLASS INSTEAD OF QUOTE.

/model.Order
- Refactor Buy method to split code according to class domain and structuring for OTC Orders.
- Refactor Sell method to split code according to class domain and structuring for OTC Orders.


################################### TESTS ###################################

/test

####### MODEL ########

/model/quote
OK - remove test__str__ method.
OK - add test for set_exchange_from_market

/model/asset
OK - create tests for model/asset

####### SERIALIZER ########

/serializer/quote
- add test for quote_serializer
ok - update markit_quote_decoder tests

/serializer/asset
- add test for asset_serializer
ok - add markit_quote_decoder tests

####### MAPPER ########
