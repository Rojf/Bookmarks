from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def setting(request):
    return render(request, 'account/settings.html', {'section': 'settings'})


class CustomPasswordChangeView(PasswordChangeView):
    success_url = '/account/settings/#account-change-password'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid password change request!')

        return HttpResponseRedirect(self.success_url)

    # Mark1q2w3e4r


class CustomPasswordResetView(PasswordResetView):
    get_url = '/account/login/#password-reset'
    success_url = reverse_lazy('login')
    redirect_authenticated_user = True
    success_authenticated_user_url = '/account/'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return HttpResponseRedirect(self.get_url)

    def dispatch(self, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.success_authenticated_user_url
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        message = "We have sent you instructions by e-mail to restore your password,"
        messages.success(self.request, message)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Fill in the e-mail fields.')

        return HttpResponseRedirect(self.get_url)
