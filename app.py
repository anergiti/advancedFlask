from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'aner'
api = Api(app)


jwt = JWT(app, authenticate, identity)
# JWT creates a new endpoint - /auth.
# when we call /auth, JWT send username and password to authenticate method.
# if authenticate method return correctly, jwt generates an auth token.
# next token is passed to identity function to get the user_id

items = []

# student inherit from Resource:
# by this class , student resource will be access only by GET method
class Item(Resource):
    #RequestParser is a field sanitator\validator:
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    # declaring @jwt_required - user must authenticate to use GET.
    # token must be passed as the header - Authorization : JWT <token>
    @jwt_required
    def get(self, name):

        item = next(filter(lambda x: x['name'] == name,items), None)
        # lambda gets two args. first is the filtering function and the other is the list
        # lambda steps:
        # 1. x['name'] == name is iterating items
        # 2. check if x matches the name and returns a filter object.
        # 3. since we need the first filered item found, we add next() and None so
        # the function wont break if there are no matches found. it will return None as response.
        # this lambda is the same action as this:

        #for item in items:
        #    if item['name'] == name:
        #        return item

        return {'item':item}, 200 if item is not None else 404

    def post(self, name):

        # if an item found and its not None:
        if next(filter(lambda x: x['name'] == name,items), None) is not None:
            return {'message': "An item with name '{}' already exists". format(name)}, 400
        # this line request.get_json() gets the data passed by the requester and interpet it to json.
        # forces the requester (endpoint\paw)
        # to pass application/json as Content-Type header. Otherwise - error.
        # optionals - data = request.get_json(force=True)
        # force=True means Content-Type is not nessecairy and the process will ignore the header. bad practice security and content integroty wise.
        # data = request.get_json(silent=True)
        # will silent an error

        # get data form the request:
        data = Item.parser.parse_args()

        #data = request.get_json()
        # get data form the request ^
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item , 201


    def delete(self, name):
        # this lambda will find all items, except the one made for deletion
        global items #point the outer items var on line 17
        items = list(filter(lambda x: x['name'] != name,items))
        return {'message':'item deleted'}

    def put(self, name):

        #data = request.get_json()
        # find if item exists:
        item = next(filter(lambda x: x['name'] == name,items), None)
        if item is None:
            # if item was not found, return the searched query
            item = {'name': name, 'price': data['price']}
            items.append(Item)
        else:
            # get data form the request:
            data = Item.parser.parse_args()
            # if item found, update the whole data dictionary:
            item.update(data)
        return item

# This class will get all items
class ItemList(Resource):
    def get(self):
        return {'items':items}


class Upload(Resource):

    def put(self):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(APP_ROOT,'files/')
        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['filedata']

        #if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        print(filename)
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        return 201


api.add_resource(Upload, '/uploadfile')


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

#debug=True is generates error debugging logging
app.run(port=5000, debug=True)
