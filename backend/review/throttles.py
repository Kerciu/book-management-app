from rest_framework.throttling import UserRateThrottle


class CommentCreateThrottle(UserRateThrottle):
    scope = "comment_create"
