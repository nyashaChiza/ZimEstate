from django.urls import path, include

from . import views

app_name = 'Zim_Estate_App'
urlpatterns = [
    path('', views.index, name='index'),

    path('search', views.search, name='search'),
    path('about', views.about, name='about'),
    path('my_account', views.my_account, name='my_account'),
    path('properties', views.properties, name='properties'),
    path('<int:id>/property_details/', views.property_details, name='property_details'),
    path('my_properties', views.my_properties, name='my_properties'),
    path('account', views.account, name='account'),
    path('upload_property', views.upload_property, name='upload_property'),
    path('property_enquiries', views.property_enquiries, name='property_enquiries'),
    path('<int:id>/edit_property', views.edit_property, name='edit_property'),
    path('<int:id>/edit_process', views.edit_process, name='edit_process'),
    path('upload_process', views.upload_process, name='upload_process'),
    path('<int:id>/buyer_process/', views.buyer_process, name='buyer_process'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('contact', views.contact, name='contact'),
    path('contact_process', views.contact_process, name='contact_process'),
    path('signup_process', views.signup_process, name='signup_process'),

]
