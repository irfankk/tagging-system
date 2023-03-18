from rest_framework import status, viewsets
from rest_framework.response import Response
from django.db.models import Case, When

from post.serializers import PostSerializer, StatusSerializer, UserListSerializer
from post.models import Post, Status



from drf_yasg.utils import swagger_auto_schema


class PostListView(viewsets.ModelViewSet):

    http_method_names = ['get']
    serializer_class = PostSerializer

    @swagger_auto_schema(
        operation_description="My API endpoint description",
        responses={
            status.HTTP_200_OK: "Success response description",
            status.HTTP_400_BAD_REQUEST: "Bad request response description",
        }
    )
    def get_queryset(self):
        liked_tags = self.request.user.user_status.filter(like=True).values_list('post__tags__tag', flat=True).distinct()
        a = Post.objects.all().exclude(status__dislike=True, status__user=self.request.user)
        suggested = Post.objects.all().order_by(
            Case(
                *[When(tags__tag=val, then=pos) for pos, val in enumerate(liked_tags)]
            )
        ).reverse()
        return suggested


class PostStatusUpdateView(viewsets.ModelViewSet):

    http_method_names = ['post']
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    @swagger_auto_schema(
        operation_description="My API endpoint description",
        responses={
            status.HTTP_200_OK: "Success response description",
            status.HTTP_400_BAD_REQUEST: "Bad request response description",
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = request.user.user_status.filter(post=serializer.validated_data.get('post'))
            if data:
                print(data)
                data[0].like = serializer.validated_data.get('like', False)
                data[0].dislike = serializer.validated_data.get('dislike', False)
                data[0].save()
            else:
                serializer.save()
            return Response({'message': 'Status updated'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikedUserListView(viewsets.ModelViewSet):
    """
    :param Info
    """

    http_method_names = ['get']
    serializer_class = UserListSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        if Post.objects.filter(id=id):
            users = Post.objects.get(id=id).status.all()
            return users
        return Response({'message': 'Invalid isd'}, status=status.HTTP_400_BAD_REQUEST)




# url: "{% url schema_url %}",
