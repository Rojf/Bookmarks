from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from account import services
from account.repositories import Repository
from django_countries import countries


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


class SettingView(View):
    success_url = '/account/settings/'
    form_types = {'social_media_user': services.social_media_form,
                  'profile': services.profile_form,
                  'info_user': services.info_user_form}

    models = {'social_media_user': Repository.SocialMediaUserRepository,
              'profile': Repository.ProfileRepository,
              'info_user': Repository.InfoUserRepository}

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        context = {
            'section': 'settings',
            'profile': services.get_profile(user=request.user.id),
            'info_user': services.get_info_user(user=request.user),
            'social_media_user': services.get_social_media_user(user=request.user.id),
            'countries': list(countries)}

        return render(request, 'account/settings.html',
                      context)

    def post(self, request):
        form_type = request.POST.get('form_type', None)

        form_class = self.form_types.get(form_type)

        if form_class:
            form = form_class(request.POST)
            if form.is_valid():
                model_update_repository = self.models.get(form_type)
                cd = form.cleaned_data

                if form_type == 'profile':
                    cd['photo'] = request.FILES.get('photo')
                    Repository.UserRepository.update(request.user, **cd)

                obj = model_update_repository.get(user=request.user)
                model_update_repository.update(obj, **cd)
            else:
                print("invalid")

        return HttpResponseRedirect(self.success_url)


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


class UserRegistration(View):
    success_url = '/account/login/'

    def post(self, request):
        user_form = services.get_registration_form(request)

        if (user_form.is_valid() and services.clean_username(user_form) and services.clean_email(user_form) and
                services.clean_password2(user_form)):
            cd = user_form.cleaned_data
            services.user_create(cd)
            print("here")
        else:
            print("Not valid")
            print(user_form.errors)
            # messages.success(self.request, )

        return HttpResponseRedirect(self.success_url)

# Mark1q2w3e4r
