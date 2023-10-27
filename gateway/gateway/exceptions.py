from nameko.exceptions import registry


def remote_error(exc_path):
    """
    Decorator that registers remote exception with matching ``exc_path``
    to be deserialized to decorated exception instance, rather than
    wrapped in ``RemoteError``.
    """

    def wrapper(exc_type):
        registry[exc_path] = exc_type
        return exc_type

    return wrapper


@remote_error('products.exceptions.NotFound')
class ProductNotFound(Exception):
    pass

@remote_error('products.exceptions.NotCreated')
class ProductNotCreated(Exception):

    pass

@remote_error('products.exceptions.NotUpdated')
class ProductNotUpdated(Exception):

    pass

@remote_error('products.exceptions.NotDeleted')
class ProductNotDeleted(Exception):

    pass

@remote_error('orders.exceptions.NotFound')
class OrderNotFound(Exception):
    pass

@remote_error('orders.exceptions.NotCreated')
class OrderNotCreated(Exception):

    pass

@remote_error('orders.exceptions.NotUpdated')
class OrderNotUpdated(Exception):

    pass

@remote_error('orders.exceptions.NotDeleted')
class OrderNotDeleted(Exception):

    pass