from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

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


from django.shortcuts import render, redirect, get_object_or_404
from backend.models import protable

def add_to_cart(request, product_id):
    product = get_object_or_404(protable, id=product_id)

    if not request.user.is_authenticated:
        return redirect()   # force login

    user_key = f"cart_{request.user.id}"  # unique cart per user

    cart = request.session.get(user_key, {})

    # If product already exists in cart, increase quantity
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'pro_name': product.pro_name,
            'price': float(product.price),
            'image': product.p_image.url,
            'quantity': 1
        }

    request.session[user_key] = cart
    request.session.modified = True

    return redirect('cart.html')
def view_cart(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user_key = f"cart_{request.user.id}"
    cart = request.session.get(user_key, {})

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    return render(request, "cart.html", {"cart": cart, "total": total})

def update_cart(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user_key = f"cart_{request.user.id}"
    cart = request.session.get(user_key, {})

    if request.method == "POST":

        # Update Quantity
        for product_id in list(cart.keys()):
            qty_key = f"quantity_{product_id}"
            if qty_key in request.POST:
                new_qty = int(request.POST[qty_key])
                if new_qty > 0:
                    cart[product_id]['quantity'] = new_qty
                else:
                    cart.pop(product_id)

        request.session[user_key] = cart
        request.session.modified = True

        # 👉 If user clicked PROCEED button
        if "proceed" in request.POST:

            # Save shipping address to session
            request.session["shipping_address"] = {
                "full_name": request.POST.get("full_name"),
                "mobile": request.POST.get("mobile"),
                "address": request.POST.get("address"),
                "city": request.POST.get("city"),
                "pincode": request.POST.get("pincode"),
                "state": request.POST.get("state"),
            }

            request.session.modified = True

            return redirect("")   # Go to payment options page

    return redirect('view_cart')




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

