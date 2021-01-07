import django_filters
from .models import IdeaModel

class IdeaFilter(django_filters.FilterSet):

    class Meta:
        model = IdeaModel
        #fields = ['topicname_idea','idea']
        fields = {
            'topicname_idea':['exact'],
            'idea': ['icontains'],
        }