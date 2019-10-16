from django.conf.urls import include, url

from . import views

urlpatterns = [
    # url(r'^(?P<account_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^$', views.index),
    url(r'^send/$', views.send, name='send'),
    url(r'^request/', views.request, name='request'),
    url(r'^importaccount/', views.importaccount, name='importaccount'),
    url(r'^get_contacts/', views.get_contacts, name='get_contacts'),
    # url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact_delete/$', views.contact_delete, name='contact_delete'),
    url(r'^contact_create/', views.contact_create, name='contact_create'),
    url(r'^accountdetails/', views.accountdetails, name='accountdetails'),
    url(r'^transactions/', views.transactions, name='transactions'),
    url(r'^offers/', views.offers, name='offers'),
    url(r'^create_account/', views.create_account, name='create_account'),
    url(r'^accounts/', views.accounts, name='accounts'),
    url(r'^get_keys/', views.keys, name='get_keys'),
    url(r'^create_fund/', views.create_fund, name='create_fund'),
    # url(r'^accountseed', views.accountseed, name='accountseed'),
    url(r'^(?P<str_addr>[A-Z,0-9]+)/$', views.detail, name='detail'),
    url(r'^qrcode_gen/', views.qrcode_gen, name='qrcode_gen'),
    url(r'contact/$',views.contact, name='contact'),
    url(r'^send_contact/', views.send_contact, name='send_contact'),
    url(r'send_payment/$', views.send_payment, name='send_payment'),
    url(r'^importaccount/$', views.importaccount, name='importaccount'),
    url(r'^admin_page/$', views.admin_page, name='admin_page'),
    url(r'^Enter_recipient/$', views.Enter_recipient, name='Enter_recipient'),
    url(r'^mobile_number/$', views.mobile_number, name='mobile_number'),
    url(r'^Email_address/$', views.Email_address, name='Email_address'),
    url(r'^verify/$', views.verify, name='verify'),
]
