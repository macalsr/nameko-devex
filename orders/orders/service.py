from nameko.events import EventDispatcher
from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from functools import lru_cache

from orders.exceptions import NotFound, NotCreated, NotDeleted, NotUpdated
from orders.models import DeclarativeBase, Order, OrderDetail
from orders.schemas import OrderSchema


class OrderServiceManager:
        db = DatabaseSession(DeclarativeBase)

        @lru_cache(maxsize=256)
        def _get_order(self,order_id):
            order = self.db.query(Order).get(order_id)
            if not order:
                raise NotFound(f"Order with ID {order_id} not found")
            return order

class OrderDetailsServiceManager:
        db = DatabaseSession(DeclarativeBase)

        def _get_order_details(self,order):
            return {od.id: od for od in order.order_details}
class OrdersService(OrderServiceManager, OrderDetailsServiceManager):
    name = 'orders'

    db = DatabaseSession(DeclarativeBase)
    event_dispatcher = EventDispatcher()

    @rpc
    def get_order(self, order_id):
        order = self._get_order(order_id)
        if not order:
            raise NotFound("Order not found")
        return OrderSchema().dump(order).data

    @rpc
    def list_orders(self,page=1, per_page=10):
        try:
            orders_query = self.db.query(Order)
            total_orders = orders_query.count()
            orders_query = orders_query.offset(int(page - 1) * int(per_page)).limit(per_page)
            orders = orders_query.all()
            orders_data = OrderSchema(many=True).dump(orders).data

            return {
                'orders': orders_data,
                'page': page,
                'per_page': per_page,
                'total_orders': total_orders,
            }
        except Exception as exc:
            raise NotFound(exc)

    @rpc
    def list_orders_filtered_by_creation_date( self, initial_date, final_date,page=1, per_page=10):
        try:
            # Convert initial_date and final_date to datetime objects, assuming they are in the ISO 8601 format
            initial_date = datetime.fromisoformat(initial_date)
            final_date = datetime.fromisoformat(final_date)

            orders_query = self.db.query(Order)

            # Apply a filter to the query to select orders within the date range
            orders_query = orders_query.filter(Order.created_at >= initial_date, Order.created_at <= final_date)

            total_orders = orders_query.count()
            orders_query = orders_query.offset(int(page - 1) * int(per_page)).limit(per_page)
            orders = orders_query.all()
            orders_data = OrderSchema(many=True).dump(orders).data
            return {
                'orders': orders_data,
                'page': page,
                'per_page': per_page,
                'total_orders': total_orders,
            }
        except Exception as exc:
            raise NotFound(exc)

    @rpc
    def create_order(self, order_details):
        try:
            order = Order(
                order_details=[
                    OrderDetail(
                        product_id=order_detail['product_id'],
                        price=order_detail['price'],
                        quantity=order_detail['quantity']
                    )
                    for order_detail in order_details
                ]
            )
            self.db.add(order)
            self.db.commit()

            order = OrderSchema().dump(order).data

            self.event_dispatcher('order_created', {
                'order': order,
            })

            return order
        except Exception as exc:
            raise NotCreated(exc)

    @rpc
    def update_order(self, order):
        order = self._get_order(order['id'])
        self._update_order_details(order,order['order_details'])
        self.db.commit()


    @rpc
    def delete_order(self, order_id):
        try:
            order = self._get_order(order_id)
            print(order)
            for order_detail in order.order_details:
                self.db.delete(order_detail)
            self.db.commit()
        except Exception as exc:
            raise NotDeleted(exc)