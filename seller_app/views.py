from django.shortcuts import render,redirect
from .models import *
from user_app.models import *

# Create your views here.
def seller_register(request):
    if request.method == "POST":
        names = request.POST.get("seller_name")
        emails = request.POST.get("email")
        passwords = request.POST.get("password")
        addresss = request.POST.get("address")
        phonenumbers = request.POST.get("phone_number")
        licenses=request.POST.get("license_number")
        data =Seller()
        data.seller_name = names
        data.email = emails
        data.password = passwords
        data.address = addresss
        data.phone_number = phonenumbers
        data.license_number = licenses
        data.save()
        return redirect('/seller_login')

    return render(request, 'seller_registration.html')
def seller_login(request):
    if request.method == "POST":
        sellername = request.POST.get("seller_name")
        password = request.POST.get("password")
        user_data = Seller.objects.filter(seller_name=sellername, password=password)
        if user_data:
            print('gvbjkk')
            for x in user_data:
                id=x.seller_id
            request.session['seller_id'] = id
            print('dgvcjv')
            return redirect('/seller/seller_home')

        else:
            print("invalid")
            return render(request, 'seller_login.html', {'status': "invalid"})
    return render(request, 'seller_login.html')

def addproduct(request):
    if 'seller_id' in request.session:
        seller_id = request.session.get("seller_id")
        print(seller_id)
        subcategories=SubCategory.objects.all()
        if request.method == "POST":
            seller_id = request.session.get("seller_id")
            print(seller_id)
            products = request.POST.get("product_name")
            descriptions = request.POST.get("description")
            prices = request.POST.get("price")
            subcategory_id = request.POST.get("subcategory")
            data = Product()
            data.product_name = products
            data.description = descriptions
            data.price = prices
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.subcategory_id = SubCategory.objects.get(subcategory_id=subcategory_id)
            data.save()
            return redirect('/')
        return render(request, 'add_product.html',{'subcategory':subcategories})
    else:
        return redirect('/seller/seller_login')

def viewpdct(request):
    product_data = Product.objects.all()
    maincategory = MainCategory.objects.prefetch_related('main').all()
    if request.method == "POST":
        search = request.POST.get('product_name')
        if search:
            product_data = Product.objects.filter(product_name__icontains=search)
    return render(request, 'viewtable.html', {'product': product_data,'main':maincategory})


def addproducthome(request):
    if 'seller_id' in request.session:
        seller_id = request.session.get("seller_id")
        print(seller_id)
        subcategories = SubCategory.objects.all()
        print(request.COOKIES)
        if request.method == "POST":
            seller_id = request.session.get("seller_id")
            print(seller_id)
            products = request.POST.get("product_name")
            descriptions = request.POST.get("description")
            prices = request.POST.get("price")
            subcategory_id = request.POST.get("subcategory")
            data = Product()
            data.product_name = products
            data.description = descriptions
            data.price = prices
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.subcategory_id = SubCategory.objects.get(subcategory_id=subcategory_id)
            data.save()
            return redirect('/')
        return render(request, 'addproducthome.html', {'subcategory': subcategories})
    else:
        return redirect('/seller/seller_login')


def producthome(request):
    if 'seller_id' in request.session:
        seller = request.session['seller_id']
        seller_data = Seller.objects.filter(seller_id=seller)
        return render(request, 'producthome.html', {'seller': seller_data})
    else:
        return redirect('/seller/seller_login')

def offerhome(request):
    if 'seller_id' in request.session:
        seller = request.session['seller_id']
        seller_data = Seller.objects.filter(seller_id=seller)
        offer = Offer.objects.all()
        if request.method == "POST":
            search = request.POST.get('product_name')
            if search:
                offer = Offer.objects.filter(product_id__product_name__icontains=search)
        return render(request, 'offerhome.html', {'offer': offer,'seller':seller_data})
    else:
        return redirect('/seller/seller_login')

def viewoffer(request):
    if 'seller_id' in request.session:
        seller = request.session['seller_id']
        offer=Offer.objects.all()
        return render(request, 'view_offer.html', {'offer':offer})
    else:
        return redirect('/seller/seller_login')

def addoffer(request,product_id):
    if 'seller_id' in request.session:
        product = Product.objects.filter(product_id=product_id)
        event=Event.objects.all()
        if request.method=="POST":
            event_id = request.POST.get('event')
            discounts=request.POST.get('discount')
            data=Offer()
            data.event_id= Event.objects.get(event_id=event_id)
            data.discount=discounts
            data.product_id = Product.objects.get(product_id=product_id)
            data.save()
            return redirect('/seller/offerhome')
        return render(request,'add_offer.html',{'offer':product,'event':event})
    else:
        return redirect('/seller/seller_login')

def edit_offer(request,offer_id):
    if 'seller_id' in request.session:
        offer= Offer.objects.filter(offer_id=offer_id)

        event=Event.objects.all()
        if request.method=="POST":
            event_id = request.POST.get('event')
            discounts=request.POST.get('discount')
            data=Offer.objects.get(offer_id=offer_id)

            data.discount=discounts

            data.save()
            return redirect('/seller/offerhome')
        return render(request,'edit_offer.html',{'offer':offer,'event':event})
    else:
        return redirect('/seller/seller_login')




# def update_offer(request):
def remove_offer(request,offer_id):
    print("remove fun called")
    product_data = Offer.objects.get(offer_id=offer_id)
    product_data.delete()
    return redirect('/seller/view_offer')


def seller_home(request):
    if 'seller_id' in request.session:
        seller=request.session['seller_id']
        seller_data=Seller.objects.filter(seller_id=seller)
        return render(request,'seller_home.html',{'seller':seller_data})
    else:
        return redirect('/seller/seller_login')

def logouts(request):
    del request.session['seller_id']
    return redirect('/seller/seller_login')

def remove(request,product_id):
    print("remove fun called")
    product_data = Product.objects.get(product_id=product_id)
    product_data.delete()
    return redirect('/seller/viewtable')


def edit(request, product_id):
    if 'seller_id' in request.session:
        seller_id = request.session.get("seller_id")
        print(seller_id)
        subcategories = SubCategory.objects.all()
        if request.method == "POST":
            seller_id = request.session.get("seller_id")
            print(seller_id)
            products = request.POST.get("product_name")
            descriptions = request.POST.get("description")
            prices = request.POST.get("price")
            subcategory_id = request.POST.get("subcategory")
            data = Product()
            data.product_name = products
            data.description = descriptions
            data.price = prices
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.subcategory_id = SubCategory.objects.get(subcategory_id=subcategory_id)
            data.save()
            return redirect('/seller/viewtable')
        product_data=Product.objects.filter(product_id=product_id)
        return render(request, 'edit_product.html', {'product':product_data,'subcategory': subcategories})
    else:
        return redirect('/seller/seller_login')


def image(request,product_id):
    if 'seller_id' in request.session:
        product = Product.objects.filter(product_id=product_id)
        if request.method == "POST":
            seller_id = request.session.get("seller_id")
            product_image = request.FILES.get("product_image")
            print('hi',product_image )
            data = Image()
            data.image = product_image
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.product_id = Product.objects.get(product_id=product_id)
            data.save()
            return redirect('/')
        return render(request, 'image.html',{'product':product} )
    else:
        return render(request, 'seller_login.html')

def speci(request,product_id):
    if 'seller_id' in request.session:
        products=Product.objects.filter(product_id=product_id)
        if request.method== "POST":
            seller_id = request.session.get("seller_id")
            colors=request.POST.get("color")
            storage=request.POST.get("storage")
            quantities=request.POST.get("quantity")
            batteries=request.POST.get("battery")
            warranties=request.POST.get("warranty")
            prices=request.POST.get("price")
            product_id=request.POST.get("product_id")
            data=Mobile()
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.color=colors
            data.storage=storage
            data.quantity=quantities
            data.battery=batteries
            data.warranty=warranties
            data.price=prices
            data.product_id = product_id
            data.save()
            return redirect('/seller/seller_home')
        return render(request, 'specification.html',{'product':products})
    else:
        return redirect('/seller/seller_login')


def seller_order(request):
    if 'seller_id' in request.session:
        seller_id = request.session.get("seller_id")
        product_details = Order.objects.filter(product_id__seller_id=seller_id)
        return render(request,'seller_order.html',{'order':product_details})
    else:
        return redirect('/seller/seller_login')

