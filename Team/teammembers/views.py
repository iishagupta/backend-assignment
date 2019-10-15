from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TeamMemberSerializer
from django.shortcuts import get_object_or_404

import json

from .models import TeamMember


class TeamMemberListView(APIView):
	def get(self, request):
		team_member_list = TeamMember.objects.all()
		serializer = TeamMemberSerializer(team_member_list, many=True)
		return JsonResponse({'team_members': serializer.data})

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

