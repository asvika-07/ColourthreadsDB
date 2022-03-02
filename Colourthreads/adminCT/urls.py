from django.urls import path
from adminCT import views as admin_views
app_name = "adminCT"

urlpatterns=[

    path("<cid>", admin_views.LoginView, name="Login"),
    path("admin/<A_id>", admin_views.AdminLogin, name="AdminLogin"),
    path("admin/all_orders_view/<aid>", admin_views.view_all_orders, name="view_orders"),
    path("admin/add_admin/<A_id>",admin_views.AddAdmin,name="Add_Admin"),
    path("admin/<A_id>/Add_products",admin_views.Add_Product,name="Add_Product"),
    path("admin/<A_id>/check_Stock",admin_views.Check_Stock,name="Check_Stock"),
    path("admin/back/<A_id>",admin_views.back,name="back"),
    path("admin/<A_id>/Add_Cat_img",admin_views.Add_Cat_Image,name="back"),
    path("add_to_cart/<cid>/<sid>/<cat>",admin_views.add_cart,name="add_cart"),
    path("like_button/<cid>/<sid>/<cat>",admin_views.like_button,name="like_button"),
    path("unlike_button/<cid>/<sid>",admin_views.remove_wishlist,name="unlike_button"),
    path("place_order/<cid>/<sid>",admin_views.order_summary,name="place_order"),
    path("place_order_success/<cid>/<sid>",admin_views.place_order,name="place_order_success"),
    
]