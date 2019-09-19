# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/3/30 19:31
from django.conf.urls import url,include

from utils.routes import CustomRouter
from api.web.search import SearchView, SuggestView

router=CustomRouter()


urlpatterns = [
    url(r'^search/$',SearchView.as_view()),
    url(r'^suggest/$',SuggestView.as_view()),
    url(r'^',include(router.urls)),
]
