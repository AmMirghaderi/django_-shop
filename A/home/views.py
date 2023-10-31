from django.shortcuts import render, redirect
from django.views import View
from . import tasks
from django.contrib import messages
from .models import Product, Category
from orders.forms import CartAddForm


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categores = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)

        return render(request, 'home/home.html', {'products': products, 'categories': categores})


class BucketHomeView(View):
    templates_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.templates_name, {'objects': objects})


class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        form = CartAddForm
        return render(request, 'home/detail.html', {'product': product, 'form': form})


class DeleteBucketObjectView(View):
    def get(self, request, key):
        tasks.delete_obj_task.delay(key)
        messages.success(request, 'delete object success', 'success')
        return redirect('home:bucket')


class DownloadbucketobjectView(View):
    def get(self, request, key):
        tasks.download_obj_task.delay(key)
        messages.success(request, 'download object success', 'success')
        return redirect('home:bucket')
