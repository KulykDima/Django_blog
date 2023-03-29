from django.urls import path

from .views import BloggerProfileView, UserConfirmEmailView
from .views import CreateNewMessage
from .views import DeleteMessage
from .views import EmailConfirmationSentView
from .views import EmailConfirmedView
from .views import EmailNotConfirmedView
from .views import Inbox
from .views import IncomingMessage
from .views import Outbox
from .views import OutgoingMessage
from .views import SendMessageFromProfileView
from .views import UserLoginView
from .views import UserLogoutView
from .views import UserProfile
from .views import UserRegistrationView
from .views import UserUpdateView

app_name = 'accounts'

urlpatterns = [
    path('register/done/', EmailConfirmationSentView.as_view(), name='register_done'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email-not-confirmed/', EmailNotConfirmedView.as_view, name='email_not_confirmed'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile_update'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/inbox', Inbox.as_view(), name='inbox'),
    path('profile/outbox', Outbox.as_view(), name='outbox'),
    path('profile/message/in/<str:pk>', IncomingMessage.as_view(), name='message'),
    path('profile/message/out/<str:pk>', OutgoingMessage.as_view(), name='out_message'),
    path('profile/message/new_message/', CreateNewMessage.as_view(), name='create_message'),
    path('profile/inbox/delete_message/<slug:id>', DeleteMessage.as_view(), name='delete_message'),
    path('profiles/user/<int:pk>', BloggerProfileView.as_view(), name='bloggers_profile'),
    path('profile/message/new_massage/<int:pk>', SendMessageFromProfileView.as_view(), name='send_message_to_blogger'),
]
