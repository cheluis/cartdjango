from django.shortcuts import render

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

class CurrentAppMixin(object):
    """
    Add a current_app property on the view and pass it to the response class.
    """
    current_app = None

    def render_to_response(self, context, **response_kwargs):
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            current_app=self.current_app,
            **response_kwargs
        )


class RedirectToMixin(object):
    """
    Provide a success_url that takes into account a request parameter (whose
    name is configurable).
    In the absence of this parameter, a (configurable) default URL is used.
    """
    redirect_field_name = REDIRECT_FIELD_NAME
    default_redirect_to = None

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_default_redirect_to(self):
        return self.default_redirect_to

    def get_success_url(self):
        default = self.get_default_redirect_to()
        redirect_to = self.request.REQUEST.get(self.get_redirect_field_name())
        return redirect_to or default


class ProtectectedRedirectToMixin(RedirectToMixin):
    """
    Ensure the URL to be redirected to is on the same host.
    """
    def get_success_url(self):
        redirect_to = super(ProtectectedRedirectToMixin, self).get_success_url()

        if not redirect_to:
            return redirect_to

        netloc = urlparse.urlparse(redirect_to)[1]

        if not netloc or netloc == self.request.get_host():
            return redirect_to

        return self.get_default_redirect_to()


class LoginView(ProtectectedRedirectToMixin, CurrentAppMixin, generic.FormView):
    """
    Displays the login form and handles the login action.
    """
    form_class = AuthenticationForm
    template_name = 'login.html'

    current_app = None
    extra_context = None

    default_redirect_to = settings.LOGIN_REDIRECT_URL

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.get_redirect_field_name(): self.get_success_url(),
            "site": current_site,
            "site_name": current_site.name,
        })

        context.update(self.extra_context or {})

        return context


class LogoutView(ProtectectedRedirectToMixin, CurrentAppMixin, generic.TemplateView):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    template_name = 'logged_out.html'

    current_app = None
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(LogoutView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            'site': current_site,
            'site_name': current_site.name,
            'title': _('Logged out')
        })
        context.update(self.extra_context or {})
        return context

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        redirect_to = self.get_success_url()

        if redirect_to is not None:
            # Redirect to the current page if no default has been provided
            redirect_to = redirect_to or self.request.path
            return HttpResponseRedirect(redirect_to)

        # Render the template
        return super(LogoutView, self).get(request, *args, **kwargs)

    # XXX: define post(), put(), ... ?


class LogoutThenLoginView(LogoutView):
    """
    Logs out the user if he is logged in. Then redirects to the log-in page.
    """
    login_url = '/login/'

    @property
    def next_page(self):
        return self.login_url or settings.LOGIN_URL