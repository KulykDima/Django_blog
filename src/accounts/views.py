from accounts.forms import ActivationLetterAgain, MessageForm, SendMessageFromProfile
from accounts.forms import UserRegisterForm
from accounts.forms import UserUpdateForm
from accounts.models import Message, User
from accounts.tasks import send_activate_email_message_task

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView
from django.views.generic import UpdateView

from post.models import Posts


class UserRegistrationView(CreateView):
    model = get_user_model()
    template_name = 'accounts/user_register.html'
    success_url = reverse_lazy('index')
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_activate_email_message_task.delay(user.id)
        return redirect('accounts:register_done')


class EmailConfirmationSentView(TemplateView):
    template_name = 'accounts/user_register_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Letter confirmation has been sent'
        return context


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_activated = True
            user.save()
            return redirect('accounts:email_confirmed')
        else:
            return redirect('accounts:email_not_confirmed')


class EmailConfirmedView(TemplateView):
    template_name = 'accounts/user_activation_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Your account has been activated'
        return context


class EmailNotConfirmedView(TemplateView):
    template_name = 'accounts/bad_signature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Troubles with the activation'
        return context


# def send_activation_letter(request):
#     form = None
#     if request.method == 'GET':
#         form = ActivationLetterAgain()
#
#     if request.method == 'POST':
#         username = request.POST.get('email')
#         user = get_object_or_404(get_user_model(), email=username)
#         form = ActivationLetterAgain(request.POST)
#         if user.is_activated:
#             return render(request, 'accounts/user_is_activated.html')
#         send_activate_email_message_task.delay(user.id)
#         return render(request, 'accounts/user_register_done.html')
#     return render(request, 'accounts/resend_email_activate.html', {'form': form})


class SendConfirmationLetterAgain(View):
    def get(self, request):
        form = ActivationLetterAgain()
        return render(self.request, 'accounts/resend_email_activate.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ActivationLetterAgain()

        if request.method == 'POST':
            form = ActivationLetterAgain(data=self.request.POST)
            if form.is_valid():
                username = request.POST.get('email')
                user = get_object_or_404(get_user_model(), email=username)
                if user.is_activated:
                    return render(self.request, 'accounts/user_is_activated.html')
                send_activate_email_message_task.delay(user.id)
                return render(self.request, 'accounts/user_register_done.html')

        return render(self.request, 'accounts/resend_email_activate.html', {'form': form})


# Отправка сообщения localhost в консоль
# def user_activate(request, sign):
#     try:
#         username = signer.unsign(sign)
#     except BadSignature:
#         return render(request, 'accounts/bad_signature.html')
#
#     user = get_object_or_404(get_user_model(), username=username)
#     if user.is_activated:
#         return render(request, 'accounts/user_is_activated.html')
#     else:
#         template = 'accounts/user_activation_done.html'
#         user.is_activated = True
#         user.is_active = True
#         user.save()
#
#     return render(request, template)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_update.html'
    model = get_user_model()
    success_url = reverse_lazy('accounts:profile')
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your profile was successfully updated')
        return response


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User {self.request.user} has logged in')

        return response


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/user_logout.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, f'User {user} successfully logged out')
        return response


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_profile.html'

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        return self.model.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['posts'] = Posts.objects.filter(author_id=self.request.user.pk).order_by('create_date')

        return context


class BloggerProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/blogger_profile_view.html'
    context_object_name = 'blogger'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['likes'] = User.objects.filter(likes__author=self.kwargs['pk']).prefetch_related('likes')
        context['dislikes'] = User.objects.filter(dislikes__author=self.kwargs['pk']).prefetch_related('dislikes')
        context['posts'] = Posts.objects.filter(author_id=self.kwargs['pk']).select_related('author')

        return context


class Inbox(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages/inbox.html'

    def get_queryset(self):
        queryset = Message.objects.filter(recipient_id=self.request.user.pk).select_related('recipient')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Inbox, self).get_context_data(**kwargs)
        context['count_of_unread'] = self.get_queryset().filter(is_readed=False).count()

        return context


class Outbox(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages/outbox.html'

    def get_queryset(self):
        queryset = Message.objects.filter(sender_id=self.request.user.pk).select_related('sender').order_by('-created')

        return queryset


class IncomingMessage(LoginRequiredMixin, View):
    def get(self, request, pk):
        private_message = Message.objects.get(id=pk)
        if not private_message.is_readed:
            private_message.is_readed = True
            private_message.save()
        return render(self.request, 'messages/message.html', {'private_message': private_message})


class OutgoingMessage(LoginRequiredMixin, View):
    def get(self, request, pk):
        sent_massage = Message.objects.get(id=pk)
        if sent_massage.is_readed:
            sent_massage.is_readed = True
            sent_massage.save()
        if not sent_massage.is_readed:
            sent_massage.is_readed = False
            sent_massage.save()

        return render(request, 'messages/out_message.html', {'sent_message': sent_massage})


class CreateNewMessage(LoginRequiredMixin, View):

    def get(self, request):
        form = MessageForm()
        return render(self.request, 'messages/message_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MessageForm()

        if request.method == 'POST':
            form = MessageForm(data=self.request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.name = request.user
                message.save()
                messages.success(self.request, 'Your message has been sent')

                return HttpResponseRedirect(reverse('accounts:inbox'))

        return render(self.request, 'messages/message_form.html', {'form': form})


class SendMessageFromProfileView(LoginRequiredMixin, View):

    def get(self, request, pk):
        recipient = get_object_or_404(User, pk=pk)
        recipient.username = recipient
        form = SendMessageFromProfile(initial={'recipient': recipient})
        return render(request, 'messages/message_form.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):
        recipient = get_object_or_404(User, pk=pk)
        recipient.username = recipient

        if request.method == 'POST':
            form = SendMessageFromProfile(initial={'recipient': recipient}, data=self.request.POST)

            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.name = request.user
                form.instance.recipient = recipient
                message.save()
                messages.success(self.request, 'Your message has been sent')
                return HttpResponseRedirect(reverse('accounts:bloggers_profile', kwargs={'pk': pk}))

        form = SendMessageFromProfile()
        return render(self.request, 'messages/message_form.html', {'form': form})


class DeleteMessage(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages/delete_message.html'
    # success_url = reverse_lazy('accounts:inbox')
    slug_field = 'id'
    slug_url_kwarg = 'id'
    success_message = "Message was deleted successfully."

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('accounts:inbox')
