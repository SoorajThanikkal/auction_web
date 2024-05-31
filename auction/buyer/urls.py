from django.urls import path
from .import views



urlpatterns = [
    path('index/',views.ind,name='index'),
    path('buyer-signup/',views.BuyerRegisterView,name='buyer-signup'),
    path('buyer-signin/',views.BuyerLoginView,name='buyer-signin'),
    path('profile/',views.BuyerProfileView,name='buyer-profile'),
    path('addprofile-buyer/',views.AddProfileView,name='addprofile'),
    path('edit-profile-buyer/',views.EditProfileView,name='editprofile'),
    path('buyerlogout/',views.BuyerLogOutView,name='buyerlogout'),
    path('delete-actn-buyer/',views.BuyerDeleteView,name='deleteactn'),
    path('add-auction/<id>/',views.AddAuctionView,name='addauction'),
    path('display-products/',views.ProductView,name='display-products'),
    path('add-to-cart/<id>/',views.AddToCartView,name='add-to-cart'),
    path('dispaly-cart/',views.DisplayCartView,name= 'dispaly-cart'),
    path('remove-cart/<id>',views.DeleteCartView,name='remove-cart'),
    path('view-winner/',views.ViewWinnerView,name='view-winner'),
    path('wins-count/', views.get_wins_count, name='wins_count'),
    path('initiate-payment/<int:product_id>/', views.initiate_payment, name='initiate-payment'),
    path('confirm-payment/<str:order_id>/<str:payment_id>/', views.confirm_payment, name='confirm-payment'),
    path('payment-success/',views.PaySuccess, name='payment-success'),
    path('my-order/',views.MyOrdersView, name='my-order'),
]
