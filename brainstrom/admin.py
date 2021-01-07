from django.contrib import admin
from .models import TopicModel,IdeaModel

class IdeaModelAdmin(admin.ModelAdmin):
    list_display = ('pk','topicname_idea','idea')
    search_fields = ('idea','topicname_idea__topicname')
    list_filter = ('topicname_idea','idea',)

    def get_queryset(self, request):
        queryset = super(IdeaModelAdmin, self).get_queryset(request)
        return queryset.order_by('pk')

admin.site.register(TopicModel)
admin.site.register(IdeaModel,IdeaModelAdmin)
