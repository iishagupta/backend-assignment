"""
	Serializers allow querysets and model instances 
	to be converted to python datatypes
	that can be rendered into JSON/ XML
"""
from rest_framework import serializers
from .models import TeamMember
from collections import OrderedDict
import re

# Stack Overlflow
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
	role =  RoleChoicesField(TeamMember.ROLE_CHOICES)

	def validate_data(self, validated_data):
		mobile = validated_data.get('mobile')
		email = validated_data.get('email')
		# 1) Begins with 0 or 91 
		# 2) Then contains 7 or 8 or 9. 
		# 3) Then contains 9 digits 
		pattern = re.compile("(0/91)?[7-9][0-9]{9}")
		if not pattern.match(mobile):
			raise serializers.ValidationError('Invalid Phone Number')
		epattern = re.compile("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")
		if not epattern.match(email):
			raise serializers.ValidationError('Invalid Email')

	def create(self, validated_data):
		self.validate_data(validated_data)
		return TeamMember.objects.create(**validated_data)

	def update(self, instance, validated_data):
		self.validate_data(validated_data)
		instance.firstName = validated_data.get('firstName', instance.firstName)
		instance.lastName = validated_data.get('lastName', instance.lastName)
		instance.email = validated_data.get('email', instance.email)
		instance.mobile = validated_data.get('mobile', instance.mobile)
		instance.role = validated_data.get('role', instance.role)
		instance.save()
		return instance
