from payment.models import Cart


def cart_context(request):
    if not request.user or not request.user.is_authenticated:
        return {"cart": None}
    
    print(request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)
    return {'cart': cart}