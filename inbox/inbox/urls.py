from cgitb import handler
from django.contrib import admin
from django.urls import path, include
from App import views
from inbox import settings
from django.conf.urls.static import static


urlpatterns = [
    # Path to access admin page
    path('admin/', admin.site.urls),

    # ================ FRONTEND ===============
    # Path to access home page (frontend)
    path('', views.home, name='home'),
    # path to send a message
    path('send_message', views.send_message, name='send_message'),

    # ================ LOGIN =================
    # Path to login/Logout
    path('login/', include('django.contrib.auth.urls')),

    # ================ BACKEND ===============
    # Path to access inbox page (backend)
    path('inbox/', views.inbox, name='inbox'),
    # Path to delete Patient
    path('delete_message/<str:customer_id>',
         views.delete_message, name="delete_message"),
    # Path to have the access to the message individually
    path('customer/<str:customer_id>', views.customer, name='customer'),
    # Path to mark the message as read
    path('mark_message', views.mark_message, name='mark_message'),
    # Path to replay the message
    path('email', views.email, name='email'),
    # Path to auto logout
    path('autologout', views.AutoLogoutUser, name='autologout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# To create ERROR pages
handler = 'App.views.E_500'
handler = 'App.views.E_404'
