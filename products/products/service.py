import logging

from nameko.events import event_handler
from nameko.rpc import rpc

from products import dependencies, schemas
from products.exceptions import NotFound, NotCreated, NotDeleted, NotUpdated


logger = logging.getLogger(__name__)


class ProductsService:

    name = 'products'

    storage = dependencies.Storage()

    @rpc
    def get(self, product_id):
        product = self.storage.get(product_id)
        if not product:
            raise NotFound("Product not found")
        return schemas.Product().dump(product).data

    @rpc
    def create(self, product):
        try:
            product = schemas.Product(strict=True).load(product).data
            self.storage.create(product)
        except Exception as exc:
            raise NotCreated(exc)

    @rpc
    def delete(self,product_id):
        try:
            self.storage.delete(product_id)
        except Exception as exc:
            raise NotDeleted(exc)
    @rpc
    def update(self,product_id,updated_fields):
        try:
            schema = schemas.UpdateProduct(strict=True)
            valid_fields = schema.load(updated_fields).data
            self.storage.update(product_id,valid_fields)
        except Exception as exc:
            raise NotUpdated(exc)


    @rpc
    def list(self, filter_title_term='', page=1, per_page=10):
        try:
            products = self.storage.list(filter_title_term, page, per_page)
            return schemas.Product(many=True).dump(products).data
        except Exception as exc:
            raise NotFound(exc)

    @event_handler('orders', 'order_created')
    def handle_order_created(self, payload):
        for product in payload['order']['order_details']:
            self.storage.decrement_stock(
                product['product_id'], product['quantity'])
