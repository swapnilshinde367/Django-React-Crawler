from rest_framework import serializers

class CrawlerSerialzer( serializers.Serializer ) :

	id = serializers.IntegerField()
	url = serializers.CharField()
	images = serializers.ListField()