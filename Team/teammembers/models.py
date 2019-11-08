from django.db import models

class TeamMember(models.Model):
	firstName = models.CharField(max_length=200, null=False, blank=False)
	lastName = models.CharField(max_length=200, null=False, blank=False)
	email = models.CharField(max_length=200, null=False, blank=False)
	mobile = models.CharField(max_length=14, null=False, blank=False)
	# Using choices field for standardization. A string other than "Admin" or "Regular" should not be entered
	ROLE_CHOICES = (
		(1, ("Admin")),
		(2, ("Regular")),
	)
	role =  models.IntegerField(choices=ROLE_CHOICES, null=False, blank=False)

	def __str__(self):
		return self.firstName + " " + self.lastName
