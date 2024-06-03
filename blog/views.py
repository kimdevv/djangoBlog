from django.shortcuts import render
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .permission import IsOwnerOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Create your views here.

'''
전체 블로그를 조회

# 함수형
@api_view(['GET', 'POST']) # GET 요청만 받겠다.
@authentication_classes([JWTAuthentication]) # JWT 인증 방식을 쓸 거다!
@permission_classes([IsAuthenticatedOrReadOnly]) # 어떤 유저만 해당 API를 사용할 수 있는지 <- Read는 가능하므로 GET은 가능.
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# 클래스형
class BlogList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
'''
# 클래스형 - 제너릭 뷰
class BlogList(ListCreateAPIView): # ListcreateAPIView는 Mixin의 ListModelMixin, CreateModelMixin 등을 다 포함하고 있음!
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user) # 기존의 perform_create에서 user 정보도 함께 저장하도록 바꿔줌!

'''
한 블로그 조회

# 함수형
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly]) # 비인가 유저는 읽기만, 인가된 유저 중 작성자만 API 사용 -> 커스텀 해야함!
def blog_detail(request, pk):
    try: # 아래 코드를 시도
        blog = Blog.objects.get(pk=pk)
        if request.method == 'GET':
            blog = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = BlogSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            blog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Blog.DoesNotExist: # 예외(오류) 발생 시 아래 코드 실행
        return Response(status=status.HTTP_404_NOT_FOUND)

# 클래스형
class BlogDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    # Blog.objects.get(pk=pk)와 동일한 기능
    def get_object(self, pk):
        blog = get_object_or_404(Blog, pk=pk)
        return blog
    
    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
# 클래스형 - 제너릭 뷰
class BlogDetail(RetrieveUpdateDestroyAPIView): # Retrieve: 특정 pk 값의 object를 불러오는 것!
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]