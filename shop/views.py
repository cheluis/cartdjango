# https://code.djangoproject.com/ticket/17209
import urlparse
import json
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from shop.models import Category, Publication


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

class Index(TemplateView):
    template_name = 'pages/index.html'
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        publications = Publication.objects.order_by('?')[:10]
        context['categories'] = categories
        context['publications'] = publications
        return context