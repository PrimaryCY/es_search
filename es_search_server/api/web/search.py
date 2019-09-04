# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/9/1 15:30
import math
from collections import Iterable

from rest_framework.views import APIView
from rest_framework.response import Response

from es_search_server.settings import es
from app.search.constant import SEARCH_TYPE_MAP


class SearchSerializer(object):
    index = 'tt_movie'

    def __init__(self, request):
        self.key_word = request.GET.get('q',None)
        self.offset = request.GET.get('offset',0)
        self.limit = request.GET.get('limit',20)
        self.type = request.GET.get('type',0)

        self.body = {}  # es请求体
        self.raw_data = {}  # es 返回的原始数据

        self.errors = None  # 错误信息

    def validate(self)->bool:
        if not self.key_word:
            self.errors = Response({
                "success": False,
                "code": "4001",
                "msg": "Wrong parameter"
            })
            return False
        if isinstance(self.offset, str):
            self.offset = int(self.offset) if self.offset.isnumeric() else 0
        if isinstance(self.limit, str):
            self.limit = int(self.limit) if self.limit.isnumeric() else 20
        if isinstance(self.type, str):
            self.type = int(self.type) if self.type.isnumeric() else 0

        self.body = self.build_body()
        assert self.body, (
            'body cannot is False'
        )
        self.raw_data = self.search()
        return True

    def build_body(self)->dict:
        query = self.build_query()
        highlight=self.build_highlight()
        size = self.limit
        offset = self.offset
        print(query)
        return {
            'query': query,
            'highlight': highlight,
            'size': size,
            'from': offset
        }

    def build_highlight(self)->dict:
        return {
            "pre_tags": '<b style="background: gainsboro;">',
            "post_tags": "</b>",
            "fields": {
                "name": {},
                "movie_desc": {}
            }
        }

    def build_query(self)->dict:
        query = {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                # {
                                #     "match": {"type": self.key_word}
                                # },
                                {
                                    "match": {"name": self.key_word}
                                },
                                {
                                    "match": {"movie_desc": self.key_word}
                                }
                            ]
                        }
                    },
                ]
            }
        }
        stype = SEARCH_TYPE_MAP.get(self.type,None)
        if stype:
            query['bool']['must'].append({
                "match_phrase_prefix": {
                        "type": stype
                    }
                }
            )
        return query

    def search(self)->Iterable:
        return es.search(index=self.index, body=self.body, filter_path=['hits.hits.highlight',
                                                                        'hits.hits._source', 'hits.total'])

    @property
    def data(self)->Iterable:
        assert self.raw_data, (
            'raw_res cannot is False'
        )
        return Response({
            'success': True,
            "code": '2000',
            "data": self.serializer_data()
        })

    def serializer_data(self)->dict:
        data = self.raw_data['hits']
        temp = []
        for i in data.get('hits', []):
            item = {k: ''.join(v) for k,v in i['highlight'].items()}
            i['_source'].update(item)
            temp.append(i['_source'])
        data['hits'] = temp
        return data


class SearchView(APIView):

    def get(self, request, *args, **kwargs):
        search = SearchSerializer(request)
        if not search.validate():
            return search.errors
        return search.data
