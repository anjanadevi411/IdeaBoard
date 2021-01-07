from django.test import TestCase
from django.urls import reverse # imports for urls test
from brainstrom.models import TopicModel,IdeaModel #import for models tests
from http import HTTPStatus

#test cases for views--------------------------------------------------------
class TopicIdeaViewPdfTestCase(TestCase):
    def test_topic_idea_render_pdf(self):
        topic_create = TopicModel.objects.create(topicname='art', author_created='anjana')
        url = reverse('pdf_format', args=(topic_create.id,))
        response = self.client.get(url)
        template_name = 'render_pdf_topic.html'
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name)

#test cases for topic list view..................................................
class TopicListViewTestCases(TestCase):
    def test_topic_list_view_no_topic(self):
        response = self.client.get(reverse('topic_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertContains(response, " ")
        self.assertTemplateUsed(response,'topic_list1.html')
        self.assertQuerysetEqual(response.context['topics'],[])

    def test_topic_list_view_with_one_topic(self):
        TopicModel.objects.create(topicname = 'art',author_created='anjana')
        response = self.client.get(reverse('topic_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'topic_list1.html')
        self.assertQuerysetEqual(response.context['topics'],['<TopicModel: art>'])

    def test_topic_list_view_with_many_topic(self):
        TopicModel.objects.create(topicname = 'art',author_created='anjana')
        TopicModel.objects.create(topicname='programming', author_created='sita')
        response = self.client.get(reverse('topic_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'topic_list1.html')
        self.assertQuerysetEqual(
            response.context['topics'],['<TopicModel: art>','<TopicModel: programming>'])

#test cases for topic detai view.................................................
class TopicDetailViewTestCase(TestCase):
    def setUp(self):
        self.topic_create = TopicModel.objects.create(topicname='art',author_created='anjana')
        self.url = reverse('topic_detail', args=(self.topic_create.id,))
        self.response = self.client.get(self.url)
        self.template_name = 'topic_detail.html'

    def test_topic_detail_view_with_topic(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response,self.template_name )
        self.assertEqual(self.response.context['topic'],self.topic_create)

    def test_topic_detail_view_with_topic_ideas(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, self.template_name)
        self.assertEqual(self.response.context['topic'], self.topic_create)
        idea_create1 = IdeaModel.objects.create(topicname_idea=self.topic_create,
                                                    idea='creativity',member_name='sita')
        url = reverse('idea_detail', args=(idea_create1.id,))
        response = self.client.get(url)
        self.assertEqual(response.context['idea'], idea_create1)

        idea_create2 = IdeaModel.objects.create(topicname_idea=self.topic_create,
                                                idea='oil painting', member_name='anjana')
        url = reverse('idea_detail', args=(idea_create2.id,))
        response = self.client.get(url)
        self.assertEqual(response.context['idea'], idea_create2)

#test cases for idea list views..................................................
class IdeaListViewTestCases(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('idea_list'))
        self.template_name = 'idea_list.html'

    def test_idea_list_view_no_idea(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response,'idea_list.html')
        self.assertQuerysetEqual(self.response.context['ideas'],[])

    def test_idea_list_view_with_one_idea(self):
        topic_create = TopicModel.objects.create(topicname = 'art',author_created='anjana')
        IdeaModel.objects.create(topicname_idea=topic_create, idea='creativity',
                                               member_name='sita')
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, self.template_name )
        self.assertQuerysetEqual(self.response.context['ideas'],['<IdeaModel: creativity>'])

    def test_idea_list_view_with_many_ideas(self):
        topic_create = TopicModel.objects.create(topicname='art',author_created='anjana')
        IdeaModel.objects.create(topicname_idea=topic_create, idea='creativity',
                                 member_name='sita')
        IdeaModel.objects.create(topicname_idea=topic_create, idea='oil painting',
                                 member_name='gita')
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, self.template_name)
        self.assertQuerysetEqual(
            self.response.context['ideas'],['<IdeaModel: creativity>','<IdeaModel: oil painting>'])

    def test_filter_set_in_context_no_data(self):
        response = self.client.get(reverse('idea_list'))
        total_ideas = response.context['ideas']
        self.assertEqual(total_ideas.count(), 0)

    def test_filter_set_in_context(self):
        topic_create1 = TopicModel.objects.create(topicname='art', author_created='anjana')
        topic_create2 = TopicModel.objects.create(topicname='animals', author_created='anjana')
        IdeaModel.objects.create(topicname_idea=topic_create1, idea='creativity',
                                     member_name='sita')
        IdeaModel.objects.create(topicname_idea=topic_create2, idea='sea animals',
                                     member_name='gita')
        IdeaModel.objects.create(topicname_idea=topic_create2, idea='land animals',
                                     member_name='gita')
        response = self.client.get(reverse('idea_list'))
        total_ideas = response.context['ideas']
        self.assertEqual(total_ideas.count(), 3)  #since total 3 idea models are there in database
        self.assertQuerysetEqual(IdeaModel.objects.filter(topicname_idea__topicname ='art'),
                                     ['<IdeaModel: creativity>'])
        self.assertQuerysetEqual(IdeaModel.objects.filter(topicname_idea__topicname ='animals'),
                                     ['<IdeaModel: land animals>','<IdeaModel: sea animals>']) #since sorted by alphabetically according to ideamodel

#test cases for idea detail view ................................................

class IdeaDetailViewTestCase(TestCase):
    def setUp(self):
        self.topic_create = TopicModel.objects.create(topicname='art',author_created='anjana')
        self.idea_create = IdeaModel.objects.create(topicname_idea=self.topic_create, idea='creativity',
                                               member_name='anju')
        url = reverse('idea_detail', args=(self.idea_create.id,))
        self.response = self.client.get(url)
        self.template_name = 'idea_detail.html'

    def test_idea_detail_view_with_topic_idea(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response,self.template_name )
        self.assertEqual(self.response.context['idea'],self.idea_create)

    def test_idea_detail_view_with_topic_idea_noideas_id(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        no_response = self.client.get('/ideadetail/1000/')
        self.assertEqual(no_response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(self.response,self.template_name)