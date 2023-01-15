from accounts.apps import user_register
from accounts.forms import ActivationLetterAgain
from accounts.forms import UserRegisterForm
from accounts.forms import UserUpdateForm
from accounts.utils import signer

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView


class UserRegistrationView(CreateView):
    model = get_user_model()
    template_name = 'accounts/user_register.html'
    success_url = reverse_lazy('accounts:register_done')
    form_class = UserRegisterForm


def send_activation_letter(request):
    form = None
    if request.method == 'GET':
        form = ActivationLetterAgain()

    if request.method == 'POST':
        username = request.POST.get('email')
        user = get_object_or_404(get_user_model(), email=username)
        print(username, user)
        form = ActivationLetterAgain(request.POST)
        if user.is_activated:
            return render(request, 'accounts/user_is_activated.html')
        user_register.send(None, instance=user)
        return render(request, 'accounts/user_register_done.html')
    return render(request, 'accounts/email_activate.html', {'form': form})


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html')

    user = get_object_or_404(get_user_model(), username=username)
    if user.is_activated:
        return render(request, 'accounts/user_is_activated.html')
    else:
        template = 'accounts/user_activation_done.html'
        user.is_activated = True
        user.is_active = True
        user.save()

    return render(request, template)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_update.html'
    model = get_user_model()
    success_url = reverse_lazy('accounts:profile')
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/user_logout.html'


def user_profile_view(request):
    return render(request, 'accounts/user_profile.html')
