from django.db.models import Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


def statistics(request):
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    total_votes = Choice.objects.aggregate(Sum("votes"))["votes_sum"] or 0
    if total_votes > 0:
        average_votes = (total_votes / total_questions)
    else:
        average_votes = 0
    most_popular_question = Question.most_popular()
    least_popular_question = Question.least_popular()
    # last_question = Question.objects.aggregate(Max("pub_date"))
    last_question = Question.objects.latest("pub_date")

    context = {
        'most_popular_question': most_popular_question,
        'least_popular_question': least_popular_question,
        'last_question': last_question,
        'total_votes': total_votes,
        'total_questions': total_questions,
        'total_choices': total_choices,
        'average_votes': average_votes,
    }
    return render(request, 'polls/statistics.html', context)


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.get_choices()
        return context


class AllQuestionView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "question_list"

    def get_queryset(self):
        """Return all the question."""
        return Question.objects.all()


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def create_question(request):
    question_text = request.POST.get("question_text")

    if not question_text:
        return render(request, "polls/create.html", )
    new_question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
    for i in range(1, 6):
        choice_text = request.POST.get(f"choice_{i}")
        if choice_text:
            Choice.objects.create(question=new_question, choice_text=choice_text)
    return HttpResponseRedirect(reverse("polls:index"))
