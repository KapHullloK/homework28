from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from ads.models import Ad
from ads.models import User

import json

from hw28_settings import settings


@method_decorator(csrf_exempt, name="dispatch")
class AdGetView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        ad_items = []

        paginator = Paginator(self.object_list.order_by('-price'), settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        for ad in page_obj:
            ad_items.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author_id": ad.author_id,
                    "author": str(User.objects.get(pk=ad.author_id)),
                    "price": ad.price,
                    "description": ad.description,
                    "is_published": ad.is_published,
                    "image": str(ad.image),
                    "category_id": ad.category_id,
                }
            )

        response = {
            "items": ad_items,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }

        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": str(User.objects.get(pk=ad.author_id)),
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": str(ad.image),
            "category_id": ad.category_id,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdPostView(CreateView):
    model = Ad
    fields = ["name", "author_id", 'price', 'description', "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author_id = ad_data["author_id"]
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.is_published = ad_data["is_published"]
        ad.image = ad_data["image"]
        ad.category_id = ad_data["category_id"]

        ad.save()

        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": str(User.objects.get(pk=ad.author_id)),
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": str(ad.image),
                "category_id": ad.category_id,
            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author_id", 'price', 'description', "is_published", "image", "category_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ads_data = json.loads(request.body)

        if ads_data.get("name"):
            self.object.name = ads_data.get("name")
        if ads_data.get("author_id"):
            self.object.author_id = ads_data.get("author_id")
        if ads_data.get("price"):
            self.object.price = ads_data.get("price")
        if ads_data.get("description"):
            self.object.description = ads_data.get("description")
        if ads_data.get("is_published", False):
            self.object.is_published = ads_data.get("is_published", False)
        if ads_data.get("category_id"):
            self.object.category_id = ads_data.get("category_id")
        if ads_data.get("image"):
            self.object.image = ads_data.get("image")

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": str(User.objects.get(pk=self.object.author_id)),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": str(self.object.image) if self.object.image else None
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UploadImagesView(UpdateView):
    model = Ad
    fields = ["name", "author_id", 'price', 'description', "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({'status': 200}, safe=False)
