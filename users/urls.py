from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    path('tutor_profile/', views.tut_profile, name='tut_profile'),
    path('profile/', views.profile, name='profile'),
    path('all_sections/', views.all_sections, name='all_sections'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_course/', views.add_course_view, name='add_course_view'),
    path('my_courses/', views.my_courses, name='my_courses'),

    path('single_course/', views.single_course, name='single_course'),
    path('update_course/', views.update_course, name='update_course'),
    path('delete_course/', views.delete_course, name='delete_course'),

    path('all_courses/', views.all_courses, name='all_courses'),
    path('cart/', views.add_to_cart, name='cart'),
    path('get_cart_data/', views.get_cart_data, name='get_cart_data'),
    path('del_cart/', views.del_cart, name='del_cart'),

    path('course/', views.course, name='course'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    #path('login/',auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    #path('logout/',auth_view.LogoutView.as_view(template_name='users/home.html'), name="logout"),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('order_history/', views.order_history, name='order_history'),

    path('content/', views.content_view, name='content'),
    path('add_content/', views.add_content_view, name='add_content'),
    path('del_content/', views.del_content, name='del_content'),

    path('workshops/', views.workshops, name='workshops'),
    path('about/', views.about, name='about'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)