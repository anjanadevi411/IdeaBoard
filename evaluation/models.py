from django.db import models

from django.db import models

class EvaluationQModel(models.Model):
    question = models.CharField(max_length=100)

    class Meta:
        ordering = ['question']

    def __str__(self):
        return self.question

class ProsModel(models.Model):
    pros = models.TextField(blank=True, null=True)
    evaluation = models.ForeignKey(EvaluationQModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pros']

    def __str__(self):
        return self.pros

class ConsModel(models.Model):
    cons = models.TextField(blank=True, null=True)
    evaluation = models.ForeignKey(EvaluationQModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['cons']

    def __str__(self):
        return self.cons