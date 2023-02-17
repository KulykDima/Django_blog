from django.urls import path
from django.views.generic import TemplateView

from .views import DeleteMessage, create_message,  inbox, message_view
from .views import UserLoginView
from .views import UserLogoutView
from .views import UserRegistrationView
from .views import UserUpdateView
from .views import send_activation_letter
from .views import user_activate
from .views import user_profile_view

app_name = 'accounts'

urlpatterns = [
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/activate_again/', send_activation_letter, name='activation_again'),
    path('register/done/', TemplateView.as_view(template_name='accounts/user_register_done.html'),
         name='register_done'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', user_profile_view, name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile_update'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/inbox', inbox, name='inbox'),
    path('profile/message/<str:pk>', message_view, name='message'),
    path('profile/message/new_message/', create_message, name='create_message'),
    path('profile/inbox/delete_message/<slug:id>', DeleteMessage.as_view(), name='delete_message'),
]
