from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from ads.models import User, Location, Ad

import json

from hw28_settings import settings


@method_decorator(csrf_exempt, name="dispatch")
class UserGetView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user_items = []

        paginator = Paginator(self.object_list, (settings.TOTAL_ON_PAGE - 5))
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        for user in page_obj:
            user_qs = Ad.objects.filter(author_id=user.id).count()
            user_items.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "role": user.role,
                    "age": user.age,
                    "locations": str(Location.objects.get(pk=user.location_id)),
                    "total_ads": user_qs,
                }
            )

        response = {
            "items": user_items,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": str(Location.objects.get(pk=user.location_id)),
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserPostView(CreateView):
    model = User
    fields = ["first_name", "last_name", 'username', 'password', "role", "age", "location_id"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        locate = Location.objects.create(
            name=', '.join(user_data["locations"]),
            lat=1.01,
            lng=5.05,
        )

        locate.save()

        user = User()
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.username = user_data["username"]
        user.password = user_data["password"]
        user.role = user_data["role"]
        user.age = user_data["age"]
        user.location_id = locate.id

        user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": str(Location.objects.get(pk=user.location_id)),
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", 'username', 'password', "role", "age", "location_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        if user_data.get("first_name"):
            self.object.first_name = user_data.get("first_name")
        if user_data.get("last_name"):
            self.object.last_name = user_data.get("last_name")
        if user_data.get("username"):
            self.object.username = user_data.get("username")
        if user_data.get("password"):
            self.object.password = user_data.get("password")
        if user_data.get("role"):
            self.object.role = user_data.get("role")
        if user_data.get("age"):
            self.object.age = user_data.get("age")
        if user_data.get("locations"):
            locate = Location.objects.get(pk=self.object.location_id)
            locate.name = ', '.join(user_data.get("locations"))
            locate.save()

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": str(Location.objects.get(pk=self.object.location_id)),
        }, safe=False)
