from django.urls import path
from django.views.generic import TemplateView
from .views import (TopicListView,TopicDetailView,create_topic_form,
                    IdeaListView,IdeaDetailView,search,create_idea_form,
                    more_ideas_formset,topic_idea_render_pdf)

urlpatterns = [
    path('topiclist/',TopicListView.as_view(),name='topic_list'),
    path ('', TemplateView.as_view(template_name = 'home.html'), name='home'),
    path('topicdetail/<int:pk>',TopicDetailView.as_view(),name='topic_detail'),
    path('topicform/', create_topic_form, name='topic_form'),
    path('ideaform/',create_idea_form,name='idea_form'),
    path('idealist/',IdeaListView.as_view(),name='idea_list'),
    path('ideadetail/<int:pk>',IdeaDetailView.as_view(),name='idea_detail'),
    path('search/',search,name='search'),
    path('<int:topicname_id>/',more_ideas_formset,name='more_ideas'),
    path('meaningfull/',TemplateView.as_view(template_name='meaningfull.html'),name='enter_meaning'),
    path('pdf_format/<int:pk>',topic_idea_render_pdf,name='pdf_format'),
]