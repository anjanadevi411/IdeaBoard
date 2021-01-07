from django.test import TestCase
from brainstrom.models import TopicModel,IdeaModel #import for models tests


# Test cases for models......................................................
class TopicModelTestCase(TestCase):
    def setUp(self):
        self.topic = TopicModel(topicname="animals", author_created="anjana") # creating a topic and saving
        self.topic.save()
        self.record = TopicModel.objects.get(pk=self.topic.id) #getting one primary key data for comparing

    def test_topic_fields(self):
        '''topic = TopicModel(topicname="animals",author_created = "anjana")
        topic.save()
        record = TopicModel.objects.get(pk=self.topic.id)'''
        self.assertEqual(self.record,self.topic)

    def test_topicname_ordering(self):
        '''topic = TopicModel.objects.create(topicname='schools', author_created='devi')
        record = TopicModel.objects.get(pk=self.topic.id)'''
        ordering = self.record._meta.ordering
        self.assertEquals(ordering[0],'topicname')


class IdeaModelTestCase(TestCase):

    def setUp(self):
        self.topic = TopicModel(topicname="animals")
        self.topic.save()
        self.idea = IdeaModel(topicname_idea=self.topic, idea="carnivorous", member_name="sita")
        self.idea.save()
        self.record = IdeaModel.objects.get(pk=self.idea.id)

    def test_Idea_fields(self):
        '''topic = TopicModel(topicname="animals")
        topic.save()
        idea = IdeaModel(topicname_idea = topic, idea = "carnivorous", member_name = "sita")
        idea.save()

        record = IdeaModel.objects.get(pk=self.idea.id)'''
        self.assertEqual(self.record,self.idea)

    def test_idea_ordering(self):
        '''topic = TopicModel.objects.create(topicname='schools', author_created='devi')
        record = TopicModel.objects.get(pk=self.topic.id)'''
        ordering = self.record._meta.ordering
        self.assertEquals(ordering[0],'idea')