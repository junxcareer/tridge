from rest_framework import pagination


class QuestionPagination(pagination.LimitOffsetPagination):
    default_limit = 5
