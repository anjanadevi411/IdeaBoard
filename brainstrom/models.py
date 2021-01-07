from django.db import models

class TopicModel(models.Model):
    topicname = models.CharField(max_length=100)
    author_created = models.CharField(max_length=30,blank=True,null=True)

    class Meta:
        #unique_together = ['topicname'] # no same topic will be created
        ordering = ['topicname']

    def __str__(self):
        return self.topicname


class IdeaModel(models.Model):
    topicname_idea = models.ForeignKey(TopicModel, related_name='topic', on_delete=models.CASCADE)
    idea = models.TextField()
    member_name = models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        #unique_together = ['idea']  # no same idea will be created
        ordering = ['idea']

    def __str__(self):
        return self.idea