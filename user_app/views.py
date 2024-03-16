from django.shortcuts import render, redirect, loader, HttpResponse
from .models import *
from seller_app.models import *
from django.db.models import Q, Sum, F
from decimal import Decimal
from django.conf import settings


import os


# Create your views here.
def user_regi(request):
    print('hi')
    if request.method == "POST":
        names = request.POST.get("user_name")
        emails = request.POST.get("email")
        passwords = request.POST.get("password")
        addresss = request.POST.get("address")
        phonenumbers = request.POST.get("phone_number")
        print(names, emails, passwords, addresss, phonenumbers)
        data = User()
        data.user_name = names
        data.email = emails
        data.password = passwords
        data.address = addresss
        data.phone_number = phonenumbers
        data.save()
        return redirect('/user_login')

    return render(request, 'user_register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("password")
        user_data = User.objects.filter(user_name=username, password=password)
        if user_data:
            for x in user_data:
                id = x.user_id
            session_timeout = getattr(settings, 'SESSION_COOKIE_AGE', 1209600)
            request.session.set_expiry(session_timeout)
            request.session['user_id'] = id
            return redirect('/')
        else:
            print("invalid")
            return render(request, 'user_login.html', {'status': "invalid"})
    return render(request, 'user_login.html')


def home(request):
    recent_visits = request.session.get('recent_visits', [])
    recent_product = Product.objects.filter(product_id__in=recent_visits)[:4]
    product_map = {product.product_id: product for product in recent_product}
    product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images','mobiles', 'tv', 'offer','headphone', 'review', 'cart').all()
    maincategory = MainCategory.objects.prefetch_related('main').all()
    new=Product.objects.all().order_by('-created_date')[:4]
    price = Product.objects.all()
    mobile=Product.objects.prefetch_related('images').filter(subcategory_id__maincategory_id=MainCategory.objects.get(maincategory_id="1"))
    laptop=Product.objects.prefetch_related('images').filter(subcategory_id__maincategory_id=MainCategory.objects.get(maincategory_id="2"))
    headphone=Product.objects.prefetch_related('images').filter(subcategory_id__maincategory_id=MainCategory.objects.get(maincategory_id="3"))
    tv=Product.objects.prefetch_related('images').filter(subcategory_id__maincategory_id=MainCategory.objects.get(maincategory_id="4"))
    print('hhh')
    user_id = request.session.get("user_id")
    user_id = User.objects.filter(user_id=user_id).first()
    if request.method == "POST":
        search = request.POST.get('product_name')
        if search:
            product_details = Product.objects.filter(Q(product_name_icontains=search) | Q(price_icontains=search))
            return render(request, 'search.html', {'search': product_details})
        elif 'price' in request.GET:
            price = request.GET['price']
            product_details = Product.objects.filter(price__lte=int(price))
            return render(request, 'search.html', {'search': product_details})
        user_id = request.session.get("user_id")
        if 'user_id' in request.session:
            if 'wishlist' in request.POST:
                print('this is for add')
                product_id = request.POST.get('product_id')
                product_id = Product.objects.get(product_id=product_id)
                data = Wishlist()
                data.user_id = User.objects.get(user_id=user_id)
                data.product_id = product_id
                data.save()
                return redirect('/')
        else:
            return redirect('/user_login')
    return render(request, 'home.html',
                  {'product': product_details, 'main': maincategory, 'arrival': new, 'mobile': mobile, 'laptop': laptop,
                   'headphone': headphone, 'tv': tv, 'user': user_id, 'recent': recent_product})

def view_product(request, product_id):
        user_id = request.session.get("user_id")
        product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images','mobiles','tv','headphone', 'review','offer',  'cart').filter(product_id=product_id)
        recent_visits = request.session.get('recent_visits', [])
        print(recent_visits)
        recent_visits.insert(0, product_id)
        print(recent_visits)
        request.session['recent_visits'] = recent_visits
        maincategory = MainCategory.objects.prefetch_related('main').all()
        if request.method == "POST":
            print(request.POST)
            if 'user_id' in request.session:
                if 'add_to_cart' in request.POST :
                    print('this is for add')
                    quantity = request.POST.get('quantity')
                    data = Cart()
                    data.user_id = User.objects.get(user_id=user_id)
                    data.product_id = Product.objects.get(product_id=product_id)
                    data.quantity = quantity
                    data.save()
                    return redirect('/cart')
                elif 'buy_now' in request.POST or "oder_btn" in request.POST:
                    print('this is buy')
                    quantity = request.POST.get('quantity')
                    address = Address.objects.filter(user_id=User.objects.get(user_id=user_id))
                    if request.method == "POST" and request.POST.get('not_go') != "Nooo":
                        print("hello buy friend")
                        quantity = request.POST.get('quantity')
                        address_id = request.POST.get('address')
                        data = Order()
                        data.user_id = User.objects.get(user_id=user_id)
                        data.quantity = quantity
                        data.product_id = Product.objects.get(product_id=product_id)
                        data.address_id = Address.objects.get(address_id=address_id)
                        data.save()
                        return redirect('/')
                    return render(request, 'order.html', {'order': product_details, 'address': address,"quantity":quantity})
            else:
                return redirect('/user_login')

        return render(request, 'view_product.html', {'product': product_details,'main':maincategory})



def cart(request):
    maincategory = MainCategory.objects.prefetch_related('main').all()
    if 'user_id' in request.session:
        product_details = Cart.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        data = product_details.values()
        print(data)
        total_price = Cart.objects.filter(user_id=User.objects.get(user_id=request.session['user_id'])).aggregate(
            total_price=Sum(F('product_id__price') * F('quantity'), output_field=models.DecimalField())
        )['total_price'] or Decimal('0.00')
        print(f"Total price for user : ₹{total_price}")
        return render(request, 'cart.html', {'cart': product_details, 'total_price': total_price,'main':maincategory})
    else:
        return redirect('/user_login')



def view_order(request):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        new = Order.objects.filter(status='pending').order_by('-order_date')
        cancel = Order.objects.filter(status='cancel').order_by('-order_date')
        order = Order.objects.filter(status='active').order_by('-order_date')
        product_details = Order.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        address=Address.objects.filter(user_id=user_id)
        total_price = Order.objects.filter(user_id=User.objects.get(user_id=request.session['user_id'])).aggregate(
            total_price=Sum(F('product_id__price') * F('quantity'), output_field=models.DecimalField())
        )['total_price'] or Decimal('0.00')
        print(f"Total price for user : ₹{total_price}")
        # if request.method == "POST":
        #     quantity=request.POST.get('quantity')
        #     address_id=request.POST.get('choose_address')
        #     data=Order()
        #     data.user_id = User.objects.get(user_id=user_id)
        #     data.quantity = quantity
        #     data.address_id=Address.objects.get(address_id=address_id)
        #     data.save()
        return render(request, 'view_order.html', {'order': product_details

            , 'address':address, 'total_price':total_price,'orders':new,'active':order,'cancel':cancel})
    else:
        return redirect('/user_login')

def cancel(request,order_id):
    order=Order.objects.get(order_id=order_id)
    order.status='cancel'
    order.save()
    return redirect('/view_order')


def discount(request):
    discount=Offer.objects.all()
    return render(request,'discount.html',{'discount':discount})

def wishlist(request):
    if 'user_id' in request.session:
        product_details = Wishlist.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'wishlist.html', {'wishlist': product_details})
    else:
        return redirect('/user_login')


def search(request):
    print('search funtn working')
    data = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images', 'mobiles', 'tv', 'headphone', 'review', 'offer', 'cart').all()
    maincategory = MainCategory.objects.prefetch_related('main').all()
    if request.method == "POST":
        search = request.POST.get('product_name')
        sort_option = request.POST.get('sort_option')
        sort_discount = request.POST.get('sort_discount')
        sort_arrival = request.POST.get('sort_arrival')
        print(sort_arrival)
        if sort_option and search:
            data = Product.objects.filter(Q(product_name__icontains=search) | Q(price__icontains=search))
            data = data.filter(price__lte=int(sort_option))
            print(search)
        elif sort_arrival and search:
            print('create with')
            data = Product.objects.filter(product_name__icontains=search)
            data=data.order_by('-created_date')
        elif sort_discount and search:
            data=Offer.objects.filter(discount__lte=int(sort_discount))
            data=data.filter(product_id__product_name__icontains=search)
            return render(request,'search.html',{'searchs':data})
        elif search:
            data = Product.objects.filter(Q(product_name__icontains=search) | Q(price__icontains=search))
        return render(request, 'search.html', {'search': data,'main':maincategory})
    return render(request, 'search.html', {'search': data,'main':maincategory })



def more(request):
    product=Product.objects.all()
    return render(request,'moreproduct.html',{'product':product})


def about(request):
    temp = loader.get_template('about.html')
    return HttpResponse(temp.render())


def viewaddress(request):
    if 'user_id' in request.session:
        product_details = Address.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'viewaddress.html', {'address': product_details})
    else:
        return redirect('/user_login')


def address(request):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            names = request.POST.get("house_name")
            city = request.POST.get("city_name")
            landmarks = request.POST.get("landmark")
            districts = request.POST.get("district")
            states = request.POST.get("state")
            post = request.POST.get("post_office")
            pins = request.POST.get("pin")
            print(names, city, landmarks, districts, states, post, pins)
            data = Address()
            data.house_name = names
            data.city_name = city
            data.landmark = landmarks
            data.district = districts
            data.state = states
            data.post_office = post
            data.pin = pins
            data.user_id = User.objects.get(user_id=user_id)
            data.save()
            return redirect('/profile')
        return render(request, 'address.html')
    else:
        return redirect('/user_login')


def profile(request):
    if 'user_id' in request.session:
        user = request.session['user_id']
        data = User.objects.filter(user_id=user)
        return render(request, 'profile.html', {'user': data})
    else:
        return redirect('/user_login')


def wel(request):
    if 'user_name' in request.session:
        user = request.session['user_name']
        print(user)
        user_data = User.objects.filter(user_name=user)
        return render(request, 'welcome.html', {'users': user_data})
    else:
        print("ooo")
        return redirect('/user_login')


def category(request, maincategory_id):
    maincategory_instance = MainCategory.objects.get(maincategory_id=maincategory_id)
    maincategory = MainCategory.objects.prefetch_related('main').all()
    print(maincategory_instance)
    product_details = Product.objects.prefetch_related('images').filter(subcategory_id__maincategory_id=maincategory_instance)
    if request.method == "POST":
        sort_option = request.POST.get('sort_option')
        sort_discount = request.POST.get('sort_discount')
        sort_arrival = request.POST.get('sort_arrival')
        if sort_option == 'low_to_high':
            product_details = product_details.order_by('price')
        elif sort_option == 'high_to_low':
            product_details = product_details.order_by('-price')
        elif sort_arrival and search:
            print('create with')
            product_details= Product.objects.prefetch_related('images').filter(subcategory_id__maincategory_id=maincategory_instance)
            product_details = product_details.order_by('-created_date')
        elif sort_discount:
            product_details = Offer.objects.filter(discount__lte=int(sort_discount))
            product_details=product_details.filter(product_id__subcategory_id__maincategory_id=maincategory_instance)
            return render(request, 'phone.html', {'discount': product_details,'main':maincategory})
    return render(request, 'phone.html', {'products': product_details,'main':maincategory})


def logout(request):
    del request.session['user_id']
    return redirect('/user_login')


def editaddress(request, address_id):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            house = request.POST.get("house_name")
            city = request.POST.get("city_name")
            land = request.POST.get("landmark")
            states = request.POST.get("district")
            districts = request.POST.get("state")
            post = request.POST.get("post_office")
            pins = request.POST.get("pin")
            data = Address.objects.get(address_id=address_id)
            data.house_name = house
            data.city_name = city
            data.landmark = land
            data.district = states
            data.state = districts
            data.post_office = post
            data.pin = pins
            data.user_id = User.objects.get(user_id=user_id)
            data.save()
            print(house, city, land, states, districts, post, pins)
            return redirect('/viewaddress')
        data = Address.objects.filter(address_id=address_id)
        return render(request, 'editaddress.html', {'datas': data})
    else:
        return redirect('/user_login')


def remove(request, address_id):
    product_data = Address.objects.get(address_id=address_id)
    product_data.delete()
    return redirect('/viewaddress')


def removes(request, cart_id):
    data = Cart.objects.get(cart_id=cart_id)
    data.delete()
    return redirect('/cart')



def addreview(request, product_id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        product = Product.objects.filter(product_id=product_id)
        if request.method == "POST":
            review = request.POST.get("review")
            data = Review()
            data.review = review
            data.user_id = User.objects.get(user_id=user_id)
            data.product_id = Product.objects.get(product_id=product_id)
            print('gfvjdv')
            data.save()
            print(f'/view_product/{product_id}')
            return redirect(f'/view_product/{product_id}')
        return render(request, 'add_review.html', {'products': product})
    else:
        return redirect('/user_login')


def review(request):
    if 'user_id' in request.session:
        review = Review.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'review.html', {'reviews': review})
    else:
        return redirect('/user_login')

def sort(request):
    if request.method == "POST":
        search = request.POST.get('product_name')
        sort_option = request.POST.get('sort_option')
        sort_discount = request.POST.get('sort_options')

        if sort_discount and search:
            data = Offer.objects.filter(discount__lte=int(sort_discount))
            data2=data.filter(product_id__product__name__icontains=search )

        elif search:
            data = Product.objects.filter(Q(product_name__icontains=search) | Q(price__icontains=search))
        return render(request, 'search.html', {'search': data})
