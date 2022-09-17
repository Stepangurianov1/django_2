
from django.urls import path

from baskets.views import read_name
from mainapp.views import products, ProductDetail

app_name = 'mainapp'
urlpatterns = [

    path('', products,name='products'),
    path('category/<int:id_category>', products, name='category'),
    path('page/<int:page>', products, name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),

]
