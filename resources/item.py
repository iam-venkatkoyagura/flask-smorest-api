import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("items", __name__, description='Operations on Items')

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not yet implemented")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating an item is not yet implemented")
    
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        item = ItemModel.query.all()
        return item
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")
                   
        return item