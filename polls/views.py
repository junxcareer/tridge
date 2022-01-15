import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import Http404
from django.utils import timezone
from django.db.models import F
from rest_framework import viewsets, filters
import django_filters

from utils.url import restify

from .models import Choice, Question, Comment
from .forms import CommentForm, ChoiceForm
from .serializers import QuestionSerializer
from .paginations import QuestionPagination


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        response = requests.get(restify("/questions/"),
                                params={"ordering": "-pub_date",
                                        # "limit": 5,
                                        # "offset": 0,
                                        "closed_at__gte": timezone.now()})

        questions = response.json()
        return questions.get('results')


class DetailView(generic.DetailView):
    template_name = "polls/detail.html"

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Question, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        choices = Choice.objects.filter(question_id=pk, approved=True)

        is_to_limit = len(choices) == self.get_object().max_choices
        context['is_to_limit'] = is_to_limit

        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.question = question
            new_comment.save()
    else:
        raise Http404('No valid access')

    return HttpResponseRedirect(reverse("polls:detail", args=(question_id,)))


def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    question = get_object_or_404(Question, pk=comment.question_id)

    if request.method == 'GET':
        return render(
            request,
            "polls/comment.html",
            {
                "comment": comment
            }
        )
    elif request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.question = question
            new_comment.parent_id = comment_id
            new_comment.save()

        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))
    else:
        raise Http404('No valid access')


def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()

    is_to_limit = len(choices) == question.max_choices

    if request.method == 'GET':
        return render(
            request,
            "polls/choice.html",
            {
                "choices": choices,
                "question": question,
                "is_to_limit": is_to_limit
            }
        )

    elif request.method == 'POST':
        if not is_to_limit:
            choice_form = ChoiceForm(data=request.POST)
            if choice_form.is_valid():
                new_choice = choice_form.save(commit=False)
                new_choice.question = question
                new_choice.save()

        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))
    else:
        raise Http404('No valid access')


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
        selected_choice.votes = F('votes') + 1
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
    pagination_class = QuestionPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter]
    filterset_fields = {"closed_at": ['gte']}
    ordering_fields = ["pub_date"]
