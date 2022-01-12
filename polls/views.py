import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import Http404
from rest_framework import viewsets, filters
import django_filters

from utils.url import restify

from .models import Choice, Question, Comment
from .forms import CommentForm
from .serializers import QuestionSerializer


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        response = requests.get(restify("/questions/"),
                                params={"ordering": "pub_date", "is_closed": False})
        questions = response.json()
        return questions[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current question to the comment
            new_comment.question = question
            # Save the comment to the database
            new_comment.save()

    else:
        raise Http404('No valid access')

    return HttpResponseRedirect(reverse("polls:detail", args=(question_id,)))


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


# API
# ===


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRestViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter]
    filterset_fields = ["is_closed"]
    ordering_fields = ["pub_date"]
