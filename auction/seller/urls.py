from django.urls import path,include
from .import views


urlpatterns = [
    
    path('seller-index/',views.SellerIndex,name='seller-index'),
    path('seller-register/',views.SellerRegister,name='seller-register'),
    path('seller-login/',views.SellerLogin,name='seller-login'),
    path('seller-profile/',views.SellerProfileView,name='seller-profile'),
    path('addprofile-seller/',views.AddSellerProfileView,name='addprofile-seller'),
    path('edit-profile-seller/',views.EditSellerProfileView,name='editprofile-seller'),
    path('seller-logout/',views.SellerLogOutView,name='seller-logout'),
    path('delete-acnt-seller/',views.SellerDeleteView,name='delete-acnt-seller'),
    path('add-product/',views.add_product,name='add-product'),
    path('product-list/',views.product_list,name='product_list'),
    path('contact/<id>/',views.BuyerContactView, name='contact'),
    path('single-pro/<id>/',views.SingleProductView, name='single_product'),
    path('pro-delete/<id>',views.ProductDeleteView, name='pro_delete'),
    path('close-auction/<id>/',views.CloseAuctionView, name='close_auction'),
    path('update-status/<int:order_id>/', views.update_status, name='update_status'),

        
]
