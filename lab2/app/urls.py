from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.order_list, name='order_list'),
    url(r'^edit/(?P<order_id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^new$', views.make_new_order, name='new'),
]

