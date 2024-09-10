from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import TemplateView

from product_module.models import Product, Category
from site_module.models import SiteSetting, FooterLinkBox, Slider, SiteBanner
from utils.convertors import group_list


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):  # Override the get_context_data method
        context = super(HomeView, self).get_context_data(**kwargs)

        latest_products = Product.objects.filter(is_active=True, is_deleted=False).order_by('-id')[:12]
        most_visited_products = Product.objects.filter(is_active=True).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        categories = list(Category.objects.annotate(product_count=Count('product_categories')).filter(is_active=True, is_deleted=False, product_count__gt=0)[:5])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)
        context['categories_products'] = categories_products
        context['sliders'] = Slider.objects.filter(is_active=True)
        context['latest_products'] = group_list(latest_products, 4)
        context['most_visited_products'] = group_list(most_visited_products, 4)

        most_bought_product = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')
        context['most_bought_products'] = group_list(list(most_bought_product), 4)

        return context


def site_header_partial(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': site_setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_partial(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    for i in footer_link_boxes:
        print(i.footerlink_set)
    context = {
        'footer_link_boxes': footer_link_boxes,
        'site_setting': site_setting,
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutUsView(TemplateView):
    template_name = 'home_module/about_us_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AboutUsView, self).get_context_data(*args, **kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.about_us)
        return context

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home_module/index_page.html' context={
#         'passed_data':data
#         })
