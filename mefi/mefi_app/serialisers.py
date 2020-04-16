from rest_framework.serializers import ModelSerializer

from .models import Taglist, Eventlist, Placelist, Eventtaglist


class TagsSerializer(ModelSerializer):
	class Meta:
		model = Taglist
		fields = ['tl_title']

class PlaceSerializer(ModelSerializer):
	class Meta:
		model = Placelist
		fields = (
		'pl_city',
		'pl_str_name',
		'pl_house_num',)


class EventSerializer(ModelSerializer):
	el_id_place = PlaceSerializer()
	class Meta:
		model = Eventlist
		fields = (
		'el_id_place',
		'el_title',
		'el_description',
		'el_date',)