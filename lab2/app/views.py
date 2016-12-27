from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .data_base import Order, Product, Stock, Client
from .forms import OrderForm, NewRecordForm

order = Order()
stock = Stock()
product = Product()
client = Client()

#order.load('orders.csv')
#stock.load('stock.csv')
#product.load('products.csv')
#lient.load('clients.csv')


def index(request):
    return HttpResponse("SuperDelivery: Order List")


def order_list(request):

    if ('search' in request.GET) and (request.GET != ''):
        key_words = request.GET['search']
        condition = "WHERE MATCH (name) AGAINST ('"
        if request.GET.get('optradio', None) == 'include':
            key_words = " ".join(['+' + item for item in key_words.split()])
            condition += key_words
        elif request.GET.get('optradio', None) == 'cost':
            key_words = key_words.strip(" ").split(" ")
            from_value = key_words[1]
            to_value = key_words[3]
            if from_value and to_value and int(from_value) <= int(to_value):
                ids = product.get_id_by_cost(from_value, to_value)
                result = tuple()
                for item in ids:
                    result += order.select_from("WHERE product_id=" + str(item))

        elif request.GET.get('optradio', None) == 'company':
            key_words = key_words.strip(" ").split(",")
            company_names = ""
            for item in key_words:
                company_names += "'" + item + "',"
            company_names = company_names[:-1]
            ids = client.get_id_by_company(company_names)
            result = tuple()
            for item in ids:
                result += order.select_from("WHERE client_id=" + str(item))

        else:
            condition += "\"" + key_words + "\""

        if request.GET.get('optradio', None) == 'include' or request.GET.get('optradio', None) == 'exclude':
            condition += "' IN BOOLEAN MODE);"
            clients = client.full_text_search(condition)
            result = tuple()
            for record in clients:
                result += order.select_from("WHERE client_id=" + str(record["id"]))
    else:
        result = order.fetch_all()

    client_name = [client.select_by_id(res["client_id"])[0]["name"] for res in result]
    product_name = [product.select_by_id(res["product_id"])[0]["name"] for res in result]

    for item, name, prod in zip(result, client_name, product_name):
        item["client_name"] = name
        item["prod_name"] = prod

    return render(request, "order_list.html", {"orders": result})


def edit(request, order_id):

    if request.method == 'POST':

        prod_id = request.POST["product_id"]
        table_row = product.select_by_id(prod_id)[0]

        if 'delete_btn' in request.POST:
            table_row["amount"] += int(request.POST["amount"])
            order.delete_by_id(order_id)
            product.update(prod_id, table_row)
            messages.add_message(request, messages.SUCCESS, 'Order was successfully deleted')
            return HttpResponseRedirect('/')

        order_form = OrderForm(request.POST)

        if order_form.is_valid() and (int(request.POST["amount"]) <= table_row["amount"]):
            data = {"product_id": request.POST["product_id"], "client_id": request.POST["client_id"],
                    "data_time": request.POST["data_time"], "amount": request.POST["amount"]}

            table_row["amount"] += order.select_by_id(order_id)[0]["amount"]
            table_row["amount"] -= int(request.POST["amount"])
            order.update(order_id, data)
            product.update(prod_id, table_row)
            messages.add_message(request, messages.SUCCESS, 'Order object updated successfully')
            return HttpResponseRedirect('/')

    record = order.select_by_id(order_id)[0]
    form = OrderForm(initial=record)
    return render(request, "edit.html", {"order_form": form})


def make_new_order(request):
    new_record_form = NewRecordForm(request.POST)
    if request.method == 'POST':
        prod_id = request.POST["product_id"]
        new_rec = product.select_by_id(prod_id)[0]
        if new_record_form.is_valid() and (int(request.POST["amount"]) <= new_rec["amount"]):
            data = {"product_id": request.POST["product_id"], "client_id": request.POST["client_id"],
                    "data_time": request.POST["data_time"], "amount": request.POST["amount"]}
            order.insert(data)
            new_rec['amount'] -= int(request.POST['amount'])
            product.update(prod_id, new_rec)
            return HttpResponseRedirect('/')

    form = NewRecordForm()
    return render(request, "new.html", {"new_rec": form})
