# https://code.djangoproject.com/ticket/17209
import urlparse
import json
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict, HttpResponse, HttpResponseRedirect, Http404 
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic import View, ListView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from shop.models import Category, Publication, Order, OrderDetail, PublicationType, PaymentMethod
from shop.forms import ProcessOrderForm, OrderDetailForm
import os
from django.utils import encoding
from django.core.mail import send_mail

# Create your views here.
class AjaxMixin(object):
    """
    This mixin is used for views which handle ajax requests because ajax request expects diffrent
    response than normal views return.
    """
    def ajax_render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request = self.request,
            template = [self.ajax_template_name],
            context = context,
            **response_kwargs
        )

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return self.ajax_render_to_response(context, **response_kwargs)
        return super(AjaxMixin, self).render_to_response(context)


class LoginRequiredMixin(object):
    """
    Mixin used for views that require a loged user
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ActiveUserOrderMixin(View):
    """
    Mixin used to get the active user order
    """
    def get_user_order(self):
        user_order = Order.objects.filter(user = self.request.user).filter(order_status = "A")
        if not user_order:
            user_order = Order(user = self.request.user)
            user_order.save()
            return user_order
        else:
            return user_order[0]

class Index(ListView, ActiveUserOrderMixin):
    """
    Entry point of the app, it displays a list of publications randomly selected
    """
    template_name = 'pages/index.html'
    model = Publication
    context_object_name = 'publications'
    queryset = Publication.objects.order_by('?')[:10]
    def get_queryset(self):
        if self.request.GET.get('category') is not None:
            return Publication.objects.filter(categories__in = self.request.GET['category'])
        else:
            return Publication.objects.order_by('?')[:10]
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        user_active_order = None
        if self.request.user.is_authenticated():
            user_active_order = self.get_user_order()
        context['order'] = user_active_order
        return context

class PublicationDetail(DetailView, ActiveUserOrderMixin):
    """
    Displays the publication detail with a form to order it
    """
    template_name = 'publication/publication-detail.html'
    model = Publication
    def get_context_data(self, **kwargs):
        context = super(PublicationDetail, self).get_context_data(**kwargs)
        related_items = self.get_related_items()
        context['publications'] = related_items
        user_active_order = None
        if self.request.user.is_authenticated():
            user_active_order = self.get_user_order()
        context['order'] = user_active_order
        form = OrderDetailForm()
        form.fields['order_presentation'].queryset = self.get_item_pub_types()
        context['form'] = form
        return context

    def get_item_pub_types(self):
        pub_types = self.object.publication_types.all()
        return pub_types

    def get_related_items(self):
        item_categories = list(self.object.categories.all())
        related_items = Publication.objects.filter(categories__in = item_categories).exclude(id = self.object.id)[:5]
        return related_items

class OrderAddDetail(UpdateView, LoginRequiredMixin):
    model = Order
    
    def post(self, request, *args, **kwargs):
        order = self.get_object()
        publication_id = self.request.POST['publication_id']
        publication = Publication.objects.get(pk = publication_id)
        qty = self.request.POST['order_quantity']
        pub_type_id = self.request.POST['order_presentation']
        pub_type = PublicationType.objects.get(pk = pub_type_id)
        order_detail = OrderDetail(order = order, order_item = publication, order_quantity = qty, order_presentation = pub_type)
        order_detail.save()
        return HttpResponseRedirect(reverse('order_detail', kwargs={'pk': order.id}))

class OrderDetailView(UpdateView, LoginRequiredMixin):
    model = Order
    template_name = 'order/order-detail.html'
    form_class = ProcessOrderForm

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order_items = OrderDetail.objects.filter(order = self.object)
        context['order_items'] = order_items
        context['order_total'] = self.get_order_total(order_items)
        return context

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order.order_address = self.request.POST['order_address']
        order.order_payment_method = PaymentMethod.objects.get(pk = self.request.POST['order_payment_method'])
        order.order_payment_number = self.request.POST['order_payment_number']
        order.order_status = 'P'
        order.save()
        #errors with the auth 
        #self.send_mail()
        return HttpResponseRedirect(reverse('order_detail', kwargs={'pk': order.id}))
    """
    This should be as a model method or in a model manager
    """
    def get_order_total(self, order_detail):
        total = 0
        for item in order_detail:
            total = total + (item.order_quantity * item.order_item.price)
        return total
    
    def send_mail(self):
        send_mail('Django Cart', 'Your order number %s has been comoppleted ' % (self.get_object().id) , 'djangosh@example.com', [self.request.user.email], fail_silently=False)

class DownloadFileView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        from django.views.static import serve
        order_detail_id = kwargs['order_detail']
        file_name = self.get_file_item_order(order_detail_id)
        if file_name == '':
            raise Http404
        filepath = "%s/%s"% (settings.MEDIA_ROOT, file_name)
        return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        
    def get_file_item_order(self, order_detail):
        order = OrderDetail.objects.get(pk = order_detail)
        print order.order_presentation.name
        if order.order_presentation.name.upper() == 'PDF':
            return order.order_item.pdf_file
        else:
            return order.order_item.audio_file