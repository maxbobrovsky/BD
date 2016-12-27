from .data_base import Order, Stock, Client, Product
from django import forms

order = Order()
client = Client()
product = Product()


class OrderForm(forms.Form):
    product_id = forms.ChoiceField(label='Product', choices=product.get_choice_lst())
    client_id = forms.ChoiceField(label='Client', choices=client.get_choice_lst())
    data_time = forms.DateTimeField(label='DateTime')
    amount = forms.IntegerField(label='Amount')


class NewRecordForm(forms.Form):
    product_id = forms.ChoiceField(label='Product', choices=product.get_choice_lst())
    client_id = forms.ChoiceField(label='Client', choices=client.get_choice_lst())
    data_time = forms.DateTimeField(label='DateTime')
    amount = forms.IntegerField(label='Amount')


