from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")


from backend.models import Contact

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )
        return render(request, "contact.html", {"success": True})

    return render(request, "contact.html")

from backend.models import pro_category
def category(request):
    data=pro_category.objects.all()
    return render(request,"category.html",{"data":data})

from django.shortcuts import render, get_object_or_404
from backend.models import pro_category , protable   # Assuming you have a Product model

def product(request, cat_id):
    category = get_object_or_404(pro_category, id=cat_id)
    products = protable.objects.filter(category=category)
    return render(request, "product.html", {"category": category, "products": products})


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from backend.models import protable
from backend.models import Cart


# ✅ Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(protable, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')



# ✅ View Cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ✅ Update Quantity
@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('view_cart')


# ✅ Remove Item
@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()

    return redirect('view_cart')



from backend.models import Order
from django.conf import settings
import razorpay

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            address=address,
            phone=phone
        )

        # Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        payment = client.order.create({
            "amount": int(total * 100),  # paise
            "currency": "INR",
            "payment_capture": 1
        })

        order.payment_id = payment['id']
        order.save()

        return render(request, "payment.html", {
            "order": order,
            "payment": payment,
            "cart_items": cart_items,
            "total": total
        })

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")

        order = Order.objects.get(payment_id=order_id)
        order.paid = True
        order.save()

        # Clear cart
        Cart.objects.filter(user=order.user).delete()

        return render(request, "success.html")

    return redirect("index")



def cart_count(request):
    if request.user.is_authenticated:
        items = Cart.objects.filter(user=request.user)
        count = sum(item.quantity for item in items)
    else:
        count = 0

    return {'cart_count': count}

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken"})

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Auto login after registration
        login(request, user)

        return redirect("index")

    return render(request, "register.html")

