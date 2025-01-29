from django.urls import path
from . import views
urlpatterns= [

    path('listings/', views.ListingView.as_view()),
    path('getlisting/', views.GetListingView.as_view()),
    path('inquiry/', views.InquiryView.as_view()),
    path('SearchListings/', views.SearchListingsView.as_view()),
    path('payment/<str:pk>', views.PaymentPageView.as_view(),name='payment'),
    path('<str:pk>', views.VerifyPaymentView.as_view()),

] 