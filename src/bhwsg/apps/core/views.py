from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django import http
from django.views.generic.base import View

from inbox.forms import InboxCreateForm
from forms import LoginForm
from utils import json


@login_required
def home(request):
    inbox_form = InboxCreateForm()
    context = {
        'inbox_form': inbox_form
    }
    return render(request, 'core/home.html', context)


def login_user(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.authenticate()
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'core/auth.html', {"form": form})


def logout_user(request):
    logout(request)
    return redirect('home')


class PermisionDenited(Exception):
    pass


class JsonView(View):
    """
        Base json protocol view.
        Used for exchanging data between frontend and backend.
    """

    def _prepare_response(self, request, *args, **kwargs):
        context = {
            'data': None,
            'message': None,
            'status': 200,
        }

        try:
            # self.prepare_context must always return dict
            context['data'] = dict(self.prepare_context(request, *args, **kwargs))
        except Exception, e:
            if isinstance(e, Http404):
                context['status'] = 404
            elif isinstance(e, PermisionDenited):
                context['status'] = 401
            else:
                context['status'] = 500
                context['message'] = e.message

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self._prepare_response(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._prepare_response(request, *args, **kwargs)

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)

    def prepare_context(self, request, *args, **kwargs):
        """ Prepare there your ansver. Must returns dict """
        return {}
