# # search/views.py

# import abc

# from django.http import HttpResponse
# from elasticsearch_dsl import Q
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.views import APIView

# from posts.documents import PostDocument
# from posts.serializers import PostSerializer


# # class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
# #     serializer_class = None
# #     document_class = None

# #     @abc.abstractmethod
# #     def generate_q_expression(self, query):
# #         """This method should be overridden
# #         and return a Q() expression."""

# #     def get(self, request, query):
# #         try:
# #             q = self.generate_q_expression(query)
# #             search = self.document_class.search().query(q)
# #             response = search.execute()

# #             print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

# #             results = self.paginate_queryset(response, request, view=self)
# #             serializer = self.serializer_class(results, many=True)
# #             return self.get_paginated_response(serializer.data)
# #         except Exception as e:
# #             return HttpResponse(e, status=500)




# # class SearchPost(PaginatedElasticSearchAPIView):
# #     serializer_class = PostSerializer
# #     document_class = PostDocument

# #     def generate_q_expression(self, query):
# #         return Q('bool',
# #                  should=[
# #                      Q('match', post=query),
                     
# #                  ], minimum_should_match=1)



# class SearchPost(APIView, LimitOffsetPagination):
#     productinventory_serializer = PostSerializer
#     search_document = PostDocument

#     def get(self, request, query=None):
#         try:
#             q = Q(
#                 "multi_match",
#                 query=query,
#                 fields=["post.body", "post.slug"],
#                 fuzziness="auto",
#             ) & Q(
#                 should=[
#                     Q("match"),
#                 ],
#                 minimum_should_match=1,
#             )

#             search = self.search_document.search().query(q)
#             response = search.execute()

#             results = self.paginate_queryset(response, request, view=self)
#             serializer = self.productinventory_serializer(results, many=True)
#             return self.get_paginated_response(serializer.data)

#         except Exception as e:
#             return HttpResponse(e, status=500)