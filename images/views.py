from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings

import redis
import requests

from images.forms import ImageCreateForm
from images.repositories.Repository import ImagesRepository
from core.utils import create_action


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
                user=request.user
            )
            new_image.image.save(image_name, ContentFile(response.content), save=True)

            create_action(request.user, 'bookmarked image', new_image)

            messages.success(request, 'Image added successfully')

            return redirect(new_image.get_absolute_url())
        else:
            print("invalid")
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.warning(request, f'{field.name} - {error}')

        return render(request, 'images/image/create.html', {'section': 'images'})


@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(ImagesRepository.model, id=id, slug=slug)
    total_views = r.incr(f'image:{image.id}:views')
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image,
                                                        'total_views': total_views})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = ImagesRepository.get(id=image_id)

            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)

            return JsonResponse({'status': 'OK'})
        except ImagesRepository.model.DoesNotExist:
            pass

    return JsonResponse({'status': 'error'})


@login_required
def images_list(request):
    images = ImagesRepository.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')

        images = paginator.page(paginator.num_pages)

    if images_only:
        return render(request,'images/image/list_images.html', {'section': 'images', 'images': images})

    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
