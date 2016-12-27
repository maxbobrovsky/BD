from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Order, Product, Stock, Client
from .forms import OrderForm
from django.db.models import Q


def index(request):
    return HttpResponse("SuperDelivery: Order List")


def order_list(request):

    if ('search' in request.GET) and (request.GET != ''):
        key_words = request.GET['search']

        if request.GET.get('optradio', None) == 'include':
            key_words = key_words.split(' ')
            if len(key_words) == 2:
                query = Q(client__name__contains=key_words[0]) | Q(client__name__contains=key_words[1])
            else:
                query = Q(client__name__contains=key_words[0])

        elif request.GET.get('optradio', None) == 'cost':
            key_words = key_words.strip(" ").split(" ")
            from_value = key_words[1]
            to_value = key_words[3]
            if from_value and to_value and int(from_value) <= int(to_value):
                result = Order.objects.filter(product__cost__range=(int(from_value), int(to_value)))

        elif request.GET.get('optradio', None) == 'company':
            key_words = key_words.strip(" ").split(",")
            print key_words
            result = Order.objects.filter(client__company__in=key_words)

        else:
            query = Q(client__name__exact=key_words)

        if request.GET.get('optradio', None) == 'include' or request.GET.get('optradio', None) == 'exclude':
            result = Order.objects.filter(query)

    else:
        result = Order.objects.all()

    return render(request, "order_list.html", {"orders": result})


def edit(request, order_id):
    if request.method == 'POST':
        if 'delete_btn' in request.POST:
            new_amount = Product.objects.get(id=request.POST["product"]).amount + int(request.POST["amount"])
            Product.objects.filter(id=request.POST["product"]).update(amount=new_amount)
            order = Order.objects.get(id=order_id)
            order.delete()
            return HttpResponseRedirect('/')

        form = OrderForm(request.POST)
        if form.is_valid():
            row = {"product": Product.objects.get(id=request.POST["product"]),
                   "client": Client.objects.get(id=request.POST["client"]), "data_time": request.POST["data_time"],
                   "amount": request.POST["amount"]}
            new_amount = Product.objects.get(id=request.POST["product"]).amount + \
                         Order.objects.get(id=order_id).amount - int(request.POST["amount"])
            Product.objects.filter(id=request.POST["product"]).update(amount=new_amount)
            Order.objects.filter(id=order_id).update(**row)
            return HttpResponseRedirect('/')

    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)
    return render(request, "edit.html", {"order_form": form})


def make_new_order(request):
    if request.method == 'POST':
        row = {"product":  Product.objects.get(id=request.POST["product"]),
               "client": Client.objects.get(id=request.POST["client"]), "data_time": request.POST["data_time"],
               "amount": request.POST["amount"]}

        new_amount = Product.objects.get(id=request.POST["product"]).amount - int(request.POST["amount"])
        Product.objects.filter(id=request.POST["product"]).update(amount=new_amount)
        order = Order(**row)
        order.save()
        return HttpResponseRedirect('/')

    form = OrderForm()
    return render(request, "new.html", {"new_rec": form})
