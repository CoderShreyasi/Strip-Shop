from django.shortcuts import render
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Product, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    products = Product.objects.all()
    orders = Order.objects.order_by('-created_at')[:20]
    return render(request, 'shop/index.html', {
        'products': products,
        'orders': orders,
        'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@require_POST
def create_checkout_session(request):
    try:
        data = request.POST
        product_id = int(data.get('product_id'))
        qty = int(data.get('quantity', '1'))
        if qty < 1:
            qty = 1
    except Exception:
        return HttpResponseBadRequest('Invalid input')


    product = Product.objects.get(id=product_id)


    # Create Stripe Checkout Session
    success_url = request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}'
    try:
        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
        'price_data': {
        'currency': 'usd',
        'product_data': {'name': product.name},
        'unit_amount': product.price_cents,
        },
        'quantity': qty,
        }],
        success_url=success_url,
        cancel_url=request.build_absolute_uri('/'),
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


    # Return session url
    return JsonResponse({'checkout_url': session.url})


def success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('index')


    # Retrieve the session to verify payment
    try:
        session = stripe.checkout.Session.retrieve(session_id, expand=['line_items'])
    except Exception:
        return redirect('index')


    if session.payment_status != 'paid':
        return redirect('index')


    # Idempotent creation: create Order only if session id not present
    order, created = Order.objects.get_or_create(
    stripe_session_id=session.id,
    defaults={'total_cents': int(sum(item.amount_total for item in session['line_items'].data))}
    )


    if created:
        # create OrderItems
        for item in session['line_items'].data:
            # description is name; quantity and price info available
            product_name = item.description
            quantity = item.quantity
            unit_price_cents = item.price.unit_amount
            # try to link to product by name (simple approach)
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                product = None
                OrderItem.objects.create(
                order=order,
                product=product,
                unit_price_cents=unit_price_cents,
                quantity=quantity,
                )


    # After ensuring order exists, redirect back to index
    return redirect('index')


