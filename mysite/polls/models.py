import datetime
from django.db import models
from django.db.models import Sum
from django.utils import timezone

MAX_LENGTH = 20


def text_excerpt(text, max_length):
    return text[:max_length] + ('...' if len(text) > max_length else '')


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return "{} {}".format(self.pub_date,
                              text_excerpt(self.question_text,
                                           MAX_LENGTH))

    def __repr__(self):
        return "<Question: {}>".format(self.question_text)
    
    @classmethod
    def most_popular(cls):
        return cls.objects.annotate(total_votes=Sum('choice__votes')) \
            .order_by('-total_votes') \
            .first()

    @classmethod
    def least_popular(cls):
        return cls.objects.annotate(total_votes=Sum('choice__votes')) \
            .order_by('total_votes') \
            .first()

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def age(self):
        return timezone.now() - self.pub_date

    def get_choices(self):
        choices = self.choice_set.all()
        total = sum(c.votes for c in choices)
        if total == 0:
            return [(c.choice_text, c.votes, 0) for c in choices]
        return [(c.choice_text, c.votes, (c.votes / total) * 100) for c in choices]

    def get_max_choice(self):
        choices = self.choice_set.all()
        if not choices:
            return None, 0
        total = sum(c.votes for c in choices)
        if total == 0:
            return None, 0
        max_choice = max(choices, key=lambda c: c.votes)
        return max_choice.choice_text, max_choice.votes / total


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return text_excerpt(self.choice_text, MAX_LENGTH)
