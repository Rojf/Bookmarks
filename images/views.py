from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_protect
from django.views import View

import requests

from images.forms import ImageCreateForm
from images.repositories.Repository import ImagesRepository


class ImageCreateViews(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'images/image/create.html', {'section': 'images'})

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request):
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            image_url = cleaned_data['url']
            name = slugify(cleaned_data['title'])
            extension = image_url.rsplit('.', 1)[1].lower()
            image_name = f'{name}.{extension}'

            response = requests.get(image_url)

            new_image, _ = ImagesRepository.create(
                title=cleaned_data['title'],
                description=cleaned_data['description'],
                url=image_url,
                user=request.user  # передаем объект пользователя
            )
            new_image.image.save(image_name, ContentFile(response.content), save=True)

            messages.success(request, 'Image added successfully')

            return redirect(new_image.get_absolute_url())
        else:
            print("invalid")
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.warning(request, f'{field.name} - {error}')

        return render(request, 'images/image/create.html', {'section': 'images'})
