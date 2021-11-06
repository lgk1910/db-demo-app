from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib import messages
import random

# Create your views here.
def index(request, id):
    return render(request, "main/home.html", {})

def home(request):
    return render(request, "main/home.html", {})

def view_books(request):
    if request.method=="POST":
        books = Book.objects.filter(book_name__contains=request.POST.get("search"))
    else:
        books = Book.objects.all()
    quantities = []
    for book in books:
        count = 0
        if len(book.hardcopy_set.all()) > 0:
            hardcopy = book.hardcopy_set.all()[0]
            for ele in hardcopy.storeinfo_set.all():
                count += ele.quantity
        quantities.append(count)
                
    return render(request, "main/books.html", {'user': request.user, 'book_quantity': zip(books, quantities)})

def product_detail(request, isbn):
    if request.method=="POST":
        if request.user.is_authenticated:
            print(request.POST)
            form = Quantity(request.POST)
            if form.is_valid():
                book = Book.objects.get(isbn=isbn)
                count = 0
                if len(book.hardcopy_set.all()) > 0:
                    hardcopy = book.hardcopy_set.all()[0]
                    for ele in hardcopy.storeinfo_set.all():
                        count += ele.quantity
                if form.cleaned_data['quantity'] > count:
                    messages.error(request, f'Exceed current stock of {book.book_name}')
                    return redirect(f'/p{isbn}')
                if request.POST.get("buy"):
                    quantity = form.cleaned_data['quantity']
                    cart = request.user.cart_set.all()[0]
                    in_cart_isbns = [cart_item.book.isbn for cart_item in cart.cartitem_set.all()]
                    if isbn in in_cart_isbns:
                        cart_item = cart.cartitem_set.get(book=book)
                        cart.total_price -= cart_item.total_price
                        if cart_item.service==0:
                            messages.info(request, 'The rent book has been removed because you want to buy new book(s)')
                            cart_item.quantity = quantity
                            cart_item.service = 1
                        else:
                            cart_item.quantity += quantity
                        cart_item.total_price = book.buy_price * cart_item.quantity
                        cart_item.save()
                        cart.total_price += cart_item.total_price
                    else:
                        cart.cartitem_set.create(book=book, quantity=quantity, total_price=quantity*book.buy_price,service=1)
                        cart.total_price += quantity*book.buy_price
                        cart.quantity+=1
                    
                    cart.save()

                    # request.user.transactioninfo_set.create(total_price=quantity*book.buy_price)
                    # trans_info = request.user.transactioninfo_set.all()[0]
                    # trans_info.transactiondetail_set.create(book=book, service=1, price=book.buy_price, quantity=quantity)
                else:
                    cart = request.user.cart_set.all()[0]
                    in_cart_isbns = [cart_item.book.isbn for cart_item in cart.cartitem_set.all()]
                    if isbn in in_cart_isbns:
                        cart_item = cart.cartitem_set.get(book=book)
                        if cart_item.service:
                            messages.info(request, 'The book you wanted to buy has been removed because you want to rent it')
                            cart.total_price = cart.total_price - cart_item.total_price + book.rent_price
                            cart_item.quantity = 1
                            cart_item.service = 0
                            cart_item.total_price = book.rent_price
                            cart_item.save()
                        messages.info(request, 'You\'ve had it in your cart')
                    else:
                        cart.cartitem_set.create(book=book, quantity=1, total_price = book.rent_price, service=0)
                        cart.total_price += book.rent_price
                        cart.quantity += 1
                    cart.save()
                    # request.user.transactioninfo_set.create(total_price=book.rent_price)
                    # trans_info = request.user.transactioninfo_set.all()[0]
                    # trans_info.transactiondetail_set.create(book=book, service=0, price=book.rent_price)
        return redirect("/cart")
    else:
        form = Quantity(initial={'quantity': 1})
        book = Book.objects.get(isbn=isbn)
        count = 0
        if len(book.hardcopy_set.all()) > 0:
            hardcopy = book.hardcopy_set.all()[0]
            for ele in hardcopy.storeinfo_set.all():
                count += ele.quantity
        return render(request, 'main/product.html', {'user': request.user, 'book': book, 'quantity': count, 'form': form})

def cart(request):
    if request.user.is_authenticated:
        cart = request.user.cart_set.all()[0]
        print(cart.total_price)
        return render(request, 'main/cart.html', {'user': request.user, 'items': cart.cartitem_set.all(), 'total_price': cart.total_price})
    else:
        messages.error(request, 'Please login to your account')
        return redirect('/login')

def change_cart(request, isbn):
    if request.user.is_authenticated:
        cart = request.user.cart_set.all()[0]
        book = Book.objects.get(isbn=isbn)
        cart_item = cart.cartitem_set.get(book=book)
        quantity = int(request.POST.get('quantity'))
        print(quantity)
        # Remove item from cart
        if quantity == 0:
            cart.total_price -= cart_item.total_price
            cart.quantity-=1
            cart_item.delete()
            cart.save()
        else:
            if cart_item.service:
                cart.total_price -= cart_item.total_price
                cart_item.quantity = quantity
                cart_item.total_price = cart_item.quantity * book.buy_price
                cart.total_price += cart_item.total_price
                cart_item.save()
                cart.save()
            else:
                messages.error(request, 'Cannot change quantity of a rent book')
        return redirect('/cart')
    else:
        messages.error(request, 'Please login to your account')
        return redirect('/login')

def remove_item_from_cart(request, isbn):
    if request.user.is_authenticated:
        cart = request.user.cart_set.all()[0]
        book = Book.objects.get(isbn=isbn)
        cart_item = cart.cartitem_set.get(book=book)
        cart.total_price -= cart_item.total_price
        cart_item.delete()
        cart.save()
        return redirect('/cart')
    else:
        messages.error(request, 'Please login to your account')
        return redirect('/login')

def insertCardInfo(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            form = InserCardInfo(request.POST)
            if form.is_valid():
                t = Card(
                    card_code=form.cleaned_data["card_code"],
                    owner_name=form.cleaned_data["owner_name"],
                    expired_date=form.cleaned_data["expired_date"],
                    branch_name=form.cleaned_data["branch_name"],
                    bank=form.cleaned_data["bank"],
                    cvv=form.cleaned_data["cvv"],
                    balance=random.choice(range(100000,500000,1000))
                )
                t.save()
                request.user.card_set.add(t)
                return HttpResponseRedirect("/home")
        else:
            return redirect('/login')
    else:
        form = InserCardInfo()
    return render(request, "main/insertcard.html", context={'user': request.user, 'form': form})

def report(request):
    if request.user.is_superuser:
        if request.method=="POST":
            form = DateForm(request.POST)
            if form.is_valid():
                trans = TransactionInfo.objects.filter(trans_date=form.cleaned_data["date"])
                sold_count = 0
                rent_count = 0
                sold_books = []
                rent_books = []
                for tran in trans:
                    trans_details = tran.transactiondetail_set.all()
                    for trans_detail in trans_details:
                        if trans_detail.service:
                            sold_count += trans_detail.quantity
                            if trans_detail.book.book_name not in sold_books:
                                sold_books.append(trans_detail.book.book_name)
                        else:
                            rent_count += 1
                            if trans_detail.book.book_name not in rent_books:
                                rent_books.append(trans_detail.book.book_name)
                return render(request, 'main/report.html', {"no_order": len(trans), 
                                                            "sold_books": sold_books,
                                                            "rent_books": rent_books,
                                                            "sold_count": sold_count,
                                                            "rent_count": rent_count,
                                                            "date": form.cleaned_data["date"]
                                                            })
        else:
            form = DateForm()
            return render(request, "main/rpquery.html", {'user': request.user, 'form': form})
    messages.error(request, 'This feature is only available to superusers')
    return redirect('/home')

def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)
        if len(request.user.card_set.all())==0:
            messages.error(request, 'You haven\'t added any card. Please add one.')
            return redirect('/insertcard')
        else:
            cards = request.user.card_set.all()
            card_infos = []
            for i, card in enumerate(cards):
                card_infos.append([i, card, '************' + str(card.card_code)[-4:]])
            cart = request.user.cart_set.all()[0]            
            return render(request, 'main/checkout.html', {'user': request.user, 'cards': card_infos, 'cart': cart})
    else:
        return redirect('/login')

def payment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            card = request.user.card_set.get(id=request.POST.get('card'))
            cart = request.user.cart_set.all()[0]
            if card.balance < cart.total_price:
                messages.error(request, 'The balance of the chosen card is not enough. Please choose another card.')
                return redirect('/checkout')

            card.balance -= cart.total_price
            card.save()
            trans_info = TransactionInfo(total_price=cart.total_price, customer=request.user)
            trans_info.save()
            request.user.transactioninfo_set.add(trans_info)
            for cart_item in cart.cartitem_set.all():
                sold_book = cart_item.book
                hardcopy = sold_book.hardcopy_set.all()[0]
                trans_info.transactiondetail_set.create(book=cart_item.book, service=cart_item.service, price=cart_item.total_price, quantity=cart_item.quantity)
                if cart_item.service:
                    for store_info in hardcopy.storeinfo_set.all():
                        if cart_item.quantity == 0:
                            break
                        if store_info.quantity < cart_item.quantity:
                            cart_item.quantity -= store_info.quantity
                            store_info.quantity = 0
                            store_info.save()
                        else:
                            store_info.quantity -= cart_item.quantity
                            cart_item.quantity = 0
                            store_info.save()
                            break

            trans_info.save() 
            request.user.cart_set.all().delete()
            request.user.cart_set.create()
            return redirect('/success')
        return redirect('/checkout')
    else:
        return redirect('/login')

def success(request):
    return render(request, 'main/success.html')
