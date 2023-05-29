from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer, UserSerializer


class UserRegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  # noqa: F841
                return Response(
                    {"message": "User registered successfully!"},
                    status=status.HTTP_201_CREATED,
                )  # noqa: E501
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_409_CONFLICT
            )  # noqa: E501


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {"id": user.id, "username": user.username}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED
        )  # noqa: E501


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful!"})


class BlogListView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.user.id)
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentCreateView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentReplyView(APIView):
    def post(self, request, comment_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            parent_comment = Comment.objects.get(pk=comment_id)
            serializer.save(parent_comment=parent_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailView(APIView):
    def get(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response(
                {"message": "Blog not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BlogSerializer(blog)
        return Response(serializer.data)
