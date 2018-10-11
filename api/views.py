# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView

from api.models import Store
from core.Mixin.StatusWrapMixin import StatusWrapMixin, ERROR_DATA
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin


class StoreListView(StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Store
    # paginate_by = 20
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        store = Store()
        for k, v in post_data.iteritems():
            setattr(store, k, v)
        try:
            store.save()
        except Exception as e:
            self.status_code = ERROR_DATA
            self.message = e
            return self.render_to_response({})
        return self.render_to_response({})


class StoreDetailView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Store
    pk_url_kwarg = 'sid'

    def post(self, request, *args, **kwargs):
        exclude = ['id']
        obj = self.get_object()
        post_data = request.POST
        for k, v in post_data.iteritems():
            if k not in exclude:
                setattr(obj, k, v)
        obj.save()
        return self.render_to_response({})