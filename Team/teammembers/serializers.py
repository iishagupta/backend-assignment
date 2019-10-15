"""
	Serializers allow querysets and model instances 
	to be converted to python datatypes
	that can be rendered into JSON/ XML
"""
from rest_framework import serializers
from .models import TeamMember
from collections import OrderedDict

class RoleChoicesField(serializers.Field): 
    def __init__(self, choices, **kwargs):
        self._choices = OrderedDict(choices)
        super(RoleChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        for i in self._choices:
            if self._choices[i] == data:
                return i
        raise serializers.ValidationError(
        	"Acceptable values are {0}.".format(list(self._choices.values())))

class TeamMemberSerializer(serializers.Serializer):
	# id = serializers.IntegerField(required=False)
	id = serializers.IntegerField(required=False)
	firstName = serializers.CharField(max_length=200)
	lastName = serializers.CharField(max_length=200)
	email = serializers.CharField(max_length=200)
	mobile = serializers.CharField(max_length=14)
	ROLE_CHOICES = (
		(1, ("Admin")),
		(2, ("Regular")),
	)
	role =  RoleChoicesField(TeamMember.ROLE_CHOICES)

	def create(self, validated_data):
		return TeamMember.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.firstName = validated_data.get('firstName', instance.firstName)
		instance.lastName = validated_data.get('lastName', instance.lastName)
		instance.email = validated_data.get('email', instance.email)
		instance.mobile = validated_data.get('mobile', instance.mobile)
		instance.role = validated_data.get('role', instance.role)
		instance.save()
		return instance