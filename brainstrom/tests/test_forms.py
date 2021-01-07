from django.test import TestCase,RequestFactory
from django.urls import reverse,resolve # imports for urls test
from django.forms import modelformset_factory
from brainstrom.models import TopicModel,IdeaModel #import for models tests
from http import HTTPStatus
from brainstrom.forms import TopicForm,IdeaForm,BaseIdeaFormset

#test cases for topic form view..................................................
class TopicCreateFormTests(TestCase):
    def setUp(self):
        TopicModel.objects.create(topicname='art',author_created='vijay')

    def test_topic_starting_lowercase(self):
        response = self.client.post(reverse('topic_form'), data={"topicname": "animals","author_created":"anjana"})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_topic_starting_uppercase(self):
        response = self.client.post(reverse('topic_form'),
                                    data={"topicname": "animals","author_created":"anjana"})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_topic_create_same_topicname_doesnot_create(self):
        response = self.client.post(reverse('topic_form'),data={"topicname": "art",
                                                                "author_created":"anjana"})
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_topic_create_form_valid(self):
        form = TopicForm(data={'topicname': 'art', 'author_created': 'anjana'})
        self.assertFalse(form.is_valid())

#test cases for idea form view..................................................
class IdeaCreateFormTests(TestCase):
    def setUp(self):
        self.topicname = TopicModel.objects.create(topicname='Art',author_created='vijay')
        self.ideaname = IdeaModel.objects.create(topicname_idea=self.topicname,
                                                 idea='water coloring',member_name='anju')

    def test_idea_starting_lowercase(self):
        '''response = self.client.post(reverse('idea_form'), data={'topicname_idea':self.topicname,
                                                    'idea':'creativity','member_name':'risheek'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)''' #to be asked to Bruno why
        form = IdeaForm(data={'topicname_idea': self.topicname, 'idea':'creativity',
        'member_name': 'anjana'})
        self.assertTrue(form.is_valid())

    def test_idea_starting_uppercase(self):
        '''response = self.client.post(reverse('idea_form'), data={'topicname_idea': self.topicname,
        'idea': 'WATER COLORING, 'member_name': 'RISHEEK'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)'''
        form = IdeaForm(data={'topicname_idea': self.topicname, 'idea':'CREATIVITY',
                              'member_name': 'ANJANA'})
        self.assertTrue(form.is_valid())

    def test_idea_create_same_topicname_doesnot_create(self):
        response = self.client.post(reverse('idea_form'),data={"topicname_idea": self.topicname,
                                                    'idea':'water coloring','member_name':'anju'})
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_idea_create_form_valid(self):
        form = IdeaForm(data={'topicname_idea': self.topicname, 'idea':'water coloring',
                              'member_name':'anju'})
        self.assertFalse(form.is_valid())

#test case for more ideas formset view ..........................................
class TestMoreIdeasFormsetView(TestCase):
    def setUp(self):
        self.topic_create = TopicModel.objects.create(topicname='art', author_created='anjana')
        self.url = reverse('more_ideas', args=(self.topic_create.id,))
        self.template_name = 'more_ideas.html'

    def test_more_ideas_formset_view(self):
        IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',), formset=BaseIdeaFormset)
        idea_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-0-topicname_idea': self.topic_create,
            'form-0-idea': 'water coloring',
            'form-1-topicname_idea': self.topic_create,
            'form-1-idea': 'creativity',
        }
        formset = IdeaFormSet(idea_data)
        response = self.client.post(self.url, data=idea_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(formset.is_valid())

    def test_more_ideas_formset_duplicate_idea_view(self):
        IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',), formset=BaseIdeaFormset)
        data_duplicate = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-topicname_idea': self.topic_create,
            'form-0-idea': 'water coloring',
            'form-1-topicname_idea': self.topic_create,
            'form-1-idea': 'creativity',
            'form-2-topicname_idea': self.topic_create,
            'form-2-idea': 'creativity',
        }
        formset = IdeaFormSet(data_duplicate)
        response = self.client.post(self.url, data=data_duplicate)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.url)
        self.assertFalse(formset.is_valid())

    def test_more_ideas_formset_messages_info(self):
        IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',), formset=BaseIdeaFormset)
        data_duplicate = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-topicname_idea': self.topic_create,
            'form-0-idea': 'water coloring',
            'form-1-topicname_idea': self.topic_create,
            'form-1-idea': 'creativity',
            'form-2-topicname_idea': self.topic_create,
            'form-2-idea': 'creativity',
        }
        formset = IdeaFormSet(data_duplicate)
        response = self.client.post(self.url, data=data_duplicate, follow=True) # use follow=True to follow redirect
        #self.assertEqual(response.status_code, HTTPStatus.OK)  # statuscode comes 200 if follow=True else statuscode is 302
        self.assertFalse(formset.is_valid())
        self.assertRedirects(response, self.url)
        # get message from context and check that expected text is there
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "info")
        self.assertTrue("Idea with the same content already exits" in message.message)

    #test cases for filters----------------------------------------------------------
'''class FilterTestCase(TestCase):
    def test_idea_filter(self):
        pass'''

#test cases for topicforms------------------------------------------------------------
class TopicFormTestCase(TestCase):
    def setUp(self):
        self.form = TopicForm(data={"topicname": "animals", "author_created": "anjana"})

    def test_topicform(self):
        self.assertTrue(self.form.is_valid())

    def test_topicform_duplicate(self):
        self.assertTrue(self.form.is_valid())
        self.form.save()
        form_duplicated = TopicForm(data={"topicname": "animals","author_created":"anjana"})
        self.assertFalse(form_duplicated.is_valid())

#test cases for ideaforms................................................................
class IdeaFormTestCase(TestCase):
    def setUp(self):
        self.topic_create = TopicModel.objects.create(topicname='art', author_created='anjana')
        self.form = IdeaForm(data={'topicname_idea': self.topic_create, 'idea': 'water coloring',
                              'member_name': 'anju'})

    def test_ideaform(self):
        self.assertTrue(self.form.is_valid())

    def test_ideaform_duplicate(self):
        self.assertTrue(self.form.is_valid())
        self.form.save()
        form_duplicated = IdeaForm(data={'topicname_idea': self.topic_create, 'idea': 'water coloring',
                              'member_name': 'anju'})
        self.assertFalse(form_duplicated.is_valid())

#test cases for baseideaformset................................................................
class BaseIdeaFormSetTestCase(TestCase):
    def test_base_idea_formset_with_zero_one_form(self):
        topic_create = TopicModel.objects.create(topicname='art', author_created='anjana')
        IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',), formset=BaseIdeaFormset)
        data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        }
        formset = IdeaFormSet(data)
        self.assertTrue(formset.is_valid())
        data_1 = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-0-topicname_idea': topic_create,
        'form-0-idea': 'water coloring',
        'form-1-topicname_idea': topic_create,
        'form-1-idea': 'creativity',
        }
        formset = IdeaFormSet(data_1)
        self.assertTrue(formset.is_valid())

    def test_base_idea_formset_duplicate_idea(self):
        topic_create = TopicModel.objects.create(topicname='art', author_created='anjana')
        IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',), formset=BaseIdeaFormset)
        data_duplicate = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-0-topicname_idea': topic_create,
            'form-0-idea': 'water coloring',
            'form-1-topicname_idea': topic_create,
            'form-1-idea': 'creativity',
            'form-2-topicname_idea': topic_create,
            'form-2-idea': 'creativity',
        }
        formset = IdeaFormSet(data_duplicate)
        self.assertFalse(formset.is_valid())
