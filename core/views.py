import requests

from django.views.generic import View
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.conf import settings


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        city = request.POST.get('city')
        if city is None:
            raise ValidationError('City is not specified')

        data = None
        error = None
        try:
            data = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.WEATHERMAP_KEY}'
            ).json()

            if data.get('cod', 200) != 200:
                error = data.get('message', 'Unknown error while fetching data')
        except Exception as e:
            error = 'An error occurred while fetching data'
            print(f'Exception: {e}')

        return render(request, 'index.html', context={'formData': request.POST, 'data': data, 'error': error})
