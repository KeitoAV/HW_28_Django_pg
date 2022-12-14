import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from HW_28_Django_postgres.settings import TOTAL_ON_PAGE
from ads.models.location import Location

from users.models import User


class UserListView(ListView):

    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        users = (self.object_list
                 .annotate(total_ads=Count('ad'))
                 .select_related('location')
                 .order_by('username')
                 )
        # pagination
        paginator = Paginator(users, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        users_on_page = paginator.get_page(page_number)

        response = {
            "items": [
                {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'age': user.age,
                    'location_id': user.location_id,
                    'location': str(user.location),
                    'total_ads': user.total_ads
                } for user in users_on_page],
            "total": paginator.count,
            "per_page": paginator.num_pages
        }

        return JsonResponse(response,
                            safe=False,
                            json_dumps_params={"ensure_ascii": False})


class UserDetailView(DetailView):

    model = User

    def get(self, *args, **kwargs):
        user = self.get_object()

        response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location_id': user.location_id,
            'location': str(user.location)
        }

        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'password', 'age', 'location']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)
        user = self.object

        user.password = user_data.get('password')
        user.first_name = user_data.get('first_name')
        user.last_name = user_data.get('last_name')
        user.age = user_data.get('age')
        location, created = Location.objects.get_or_create(name=user_data.get('location'))
        user.location = location

        user.save()

        response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location_id': user.location_id,
            'location': str(user.location)
        }

        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'},
                            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):

    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'password', 'age', 'location']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        user = User.objects.create(
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role=user_data.get('role'),
            password=user_data.get('password'),
            age=user_data.get('age')
        )

        location, created = Location.objects.get_or_create(name=user_data.get('location'))
        user.location = location
        user.save()

        response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location_id': user.location_id,
            'location': str(user.location)
        }

        return JsonResponse(response, safe=False,
                            json_dumps_params={"ensure_ascii": False})

