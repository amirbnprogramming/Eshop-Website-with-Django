from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from site_module.models import SiteBanner
from utils.convertors import group_list
from utils.http_service import get_client_ip
from .models import Product, Category, Brand, ProductVisit, ProductGallery




class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product  # we should not pass the instance just Class name of model
    context_object_name = 'products'
    ordering = ['-price']  # order by what? which fields ? we can specify it with list of fields
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()  # maximum price
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.product_list)

        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')

        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        elif brand_name is not None:
            query = query.filter(brand__url_name__iexact=brand_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product  # select which model is under exploring
    '''
    select which item of model is a key (which product) by just only id or slug
    we should pass <int:pk> or <slug:slug> in path 
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.product_detail)
        galleries = list(ProductGallery.objects.filter(is_active=True, product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_gallery'] = group_list(galleries, 3)

        related_products = list(Product.objects.filter(is_active=True, brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12])
        context['related_products_by_brand'] = group_list(related_products, 3)

        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product=loaded_product).exists()
        if not has_been_visited:
            new_product_visit = ProductVisit()
            new_product_visit.user_id = user_id
            new_product_visit.product_id = loaded_product.id
            new_product_visit.ip = user_ip
            new_product_visit.save()

        return context


class AddProductFavoriteView(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorites"] = product_id
        return redirect(product.get_absolute_url())


def product_categories_component(request):
    product_categories = Category.objects.filter(is_active=True, is_deleted=False).all()
    context = {
        'product_categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request):
    product_brands = Brand.objects.annotate(product_count=Count('product')).filter(is_active=True,
                                                                                   is_deleted=False).all()
    context = {
        'product_brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)


# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductListView, self).get_context_data(**kwargs)
#         context['products'] = Product.objects.all().order_by('-price')[:5]
#         return context


# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#         context['product'] = get_object_or_404(Product, slug=kwargs['url_slug'])
#         return context


'''function base view'''

# def product_list(request):
#     product_collection = Product.objects.all().order_by('-price')[:5]
#
#     return render(request, 'product_module/product_list.html', context={
#         'products': product_collection,
#     })
#

# def product_detail(request, url_slug):
#     try:
#         selected_product = Product.objects.get(slug=url_slug)
#     except Product.DoesNotExist:
#         raise Http404()
#
#     # selected_product = get_object_or_404(Product, slug=url_slug)
#
#     return render(request, 'product_module/product_detail.html', context={
#         'product': selected_product
#     })

# def product_list(request):
#     product_collection = Product.objects.all()
#     return render(request, 'product_module/product_list.html', context={
#         'products': product_collection
#     })
