from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TeamMemberSerializer
from django.shortcuts import get_object_or_404
from rest_framework.settings import api_settings

import json

from .models import TeamMember


class TeamMemberListView(APIView):
	queryset = TeamMember.objects.all()
	serializer_class = TeamMemberSerializer
	pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

	def get(self, request):
		page = self.paginate_queryset(self.queryset)
	 	if page is not None:
	        serializer = self.serializer_class(page, many=True)
	        return self.get_paginated_response(serializer.data)

	def post(self, request):
		team_member = request.data.get('team_member')
		serializer = TeamMemberSerializer(data=team_member)
		if serializer.is_valid(raise_exception=True):
			team_member_saved = serializer.save()
		return JsonResponse(TeamMemberSerializer(team_member_saved).data)

	def put(self, request, pk):
		saved_team_member = get_object_or_404(TeamMember, id=pk)
		data = request.data.get('team_member')
		serializer = TeamMemberSerializer(instance=saved_team_member, data=data, partial=True)
		if serializer.is_valid(raise_exception=True):
			team_member_saved = serializer.save()
		return JsonResponse(TeamMemberSerializer(team_member_saved).data)

	def delete(self, request, pk):
		team_member = get_object_or_404(TeamMember.objects.all(), id=pk)
		team_member.delete()
		return JsonResponse({"result": []})

	@property
	def paginator(self):
	    """
	    The paginator instance associated with the view, or `None`.
	    """
	    if not hasattr(self, '_paginator'):
	        if self.pagination_class is None:
	            self._paginator = None
	        else:
	            self._paginator = self.pagination_class()

	def paginate_queryset(self, queryset):
	     """
	     Return a single page of results, or `None` if pagination is disabled.
	     """
	     if self.paginator is None:
	         return None
	     return self.paginator.paginate_queryset(queryset, self.request, view=self)

	def get_paginated_response(self, data):
	     """
	     Return a paginated style `Response` object for the given output data.
	     """
	     assert self.paginator is not None
	     return self.paginator.get_paginated_response(data)