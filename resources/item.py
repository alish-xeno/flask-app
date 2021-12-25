# import sqlite3
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be empty!"
    )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "sn item with name '{}' already exists".format(name)}, 404
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except Exception as e:
            print(e)
            return {"Message": "An error occured inserting the item"}, 500
       
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}
        '''
            The code below for delete is replaced by SQLAlchemy code above
        '''
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)            
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        
        # using list comprehenson
        return {"items": [item.json() for item in ItemModel.query.all()]}

        # using lambda function
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}

        # using old sqlite3
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name": row[0], "price": row[1]})

        # connection.close()

        # return {"items": items}
