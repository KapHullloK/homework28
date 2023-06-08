from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json


##################### |
DATA_FOR_LOAD = None
##################### |


@method_decorator(csrf_exempt, name="dispatch")
class StatusView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


# TODO unsafe !!!
@method_decorator(csrf_exempt, name="dispatch")
class DownloadDataView(View):
    def get(self, request):
        with open('datasets/category.json', 'r') as file:
            data = json.load(file)

            for item in data:
                result = DATA_FOR_LOAD(name=item['name'])
                result.save()

        return JsonResponse({"status": "ok"}, status=200)
