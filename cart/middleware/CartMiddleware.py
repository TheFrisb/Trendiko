from cart.models import Cart


class CartMiddleware:
    """Cart Middleware"""

    def __init__(self, get_response):
        """Middleware Initialization"""
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware Call to create or get the cart

        Authenticated carts ( there are only admins in this project ) are still
        based on a session key.
        Cart model has a user field, should they choose to expand in the future.

        :param request:
        :return:
        """
        session_key = request.session.session_key
        if session_key is None:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(session_key=session_key)

        if not created:
            cart = (
                Cart.objects.filter(id=cart.id).prefetch_related("cart_items").first()
            )
        request.cart = cart

        response = self.get_response(request)
        return response
