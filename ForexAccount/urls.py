from django.urls import path, include
import ForexAccount.views

urlpatterns=[
    path('index',ForexAccount.views.get_index_page),
    path('account_result',ForexAccount.views.get_account_result_page)
]