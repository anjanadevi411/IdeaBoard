from django.test import TestCase,RequestFactory
from django.urls import reverse,resolve # imports for urls test
from brainstrom.views import (create_topic_form,TopicListView,TopicDetailView,create_idea_form,
                    IdeaListView,IdeaDetailView,topic_idea_render_pdf,more_ideas_formset)


#test cases for urls.........................................................
class UrlsTopicTestCase(TestCase):
    def test_topicform(self):
        url = reverse('topic_form')
        #print(resolve(url))
        self.assertEqual(resolve(url).func,create_topic_form)

    def test_topiclist(self):
        url = reverse('topic_list')
        self.assertEqual(resolve(url).func.view_class,TopicListView)

    def test_topicdetail(self):
        url = reverse('topic_detail',args=[1])
        self.assertEqual(resolve(url).func.view_class,TopicDetailView)

    def test_pdfformat(self):
        url = reverse('pdf_format',args=[1])
        self.assertEqual(resolve(url).func,topic_idea_render_pdf)


class UrlsIdeaTestCase(TestCase):
    def test_Ideaform(self):
        url = reverse('idea_form')
        #print(resolve(url))
        self.assertEqual(resolve(url).func,create_idea_form)

    def test_idealist(self):
        url = reverse('idea_list')
        self.assertEqual(resolve(url).func.view_class,IdeaListView)

    def test_Ideadetail(self):
        url = reverse('idea_detail',args=[1])
        self.assertEqual(resolve(url).func.view_class,IdeaDetailView)

    def test_moreidea(self):
        url = reverse('more_ideas',args=[1])
        self.assertEqual(resolve(url).func,more_ideas_formset)