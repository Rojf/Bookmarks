from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from django_countries import countries

from core.repositories.Repository import UserRepository
from actions.utils import create_action
from actions.repositories import Repository
from account.repositories import Repository
from account import services
from account import forms


@login_required
def dashboard(request):
    actions = Repository.ActionRepository.model.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.fillter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


class SettingView(View):
    success_url = '/account/settings/'
    form_types = {'social_media_user': forms.SocialMediaUserForm,
                  'profile': forms.ProfileForm,
                  'info_user': forms.InfoUserForm}

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
            'profile': Repository.ProfileRepository.get(user=request.user),
            'info_user': Repository.InfoUserRepository.get(user=request.user),
            'social_media_user': Repository.SocialMediaUserRepository.get(user=request.user.id),
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
                    UserRepository.update(request.user, **cd)

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
        user_form = forms.RegistrationForm(request.POST)

        if (user_form.is_valid() and services.clean_username(user_form) and services.clean_email(user_form) and
                services.clean_password2(user_form)):
            cd = user_form.cleaned_data

            user = services.user_create(cd)

            Repository.ProfileRepository.create(user=user)
            Repository.InfoUserRepository.create(user=user)
            Repository.SocialMediaUserRepository.create(user=user)

            create_action(user, 'has created an account')
            messages.success(self.request, 'You have created an account.')
        else:
            print("Not valid")
            # messages.warning(self.request, 'Data not valid')

        return HttpResponseRedirect(self.success_url)
# Mark1q2w3e4r


@login_required
def user_list(request):
    users = UserRepository.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(UserRepository.model, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    active = request.POST.get('active')
    if user_id and active:
        try:
            user = UserRepository.get(id=user_id)
            if active == 'follow':
                Repository.ContactRepository.create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            elif active == 'unfollow':
                Repository.ContactRepository.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except UserRepository.model.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})
