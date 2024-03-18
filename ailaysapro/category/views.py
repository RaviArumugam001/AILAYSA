from django.db.models import Max
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework import serializers
from rest_framework.response import Response
import json,random,time
from rest_framework import serializers
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from rest_framework.views import APIView

from category.models import Category, Subcategory, Song, Artist, CommentModel, PostModel


# Create your views here.
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields="__all__"

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)
    class Meta:
        model = Category
        fields="__all__"


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'name')


class ArtistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'songs')

# @csrf_exempt
# def catsubcatlistdata(request):
class CategoryListView(APIView):
    def get(self,request):
        if request.method=='get' or request.method=='GET':
            try:
                data=Category.objects.all()
                serial=CategorySerializer(data,many=True)


                return Response(serial.data)
            except Exception as e:
                err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
                return HttpResponse(json.dumps(err), content_type="application/json")
        else:

            err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
            return HttpResponse(json.dumps(err), content_type="application/json")
class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['id', 'comment', 'publication_date']

class PostModelSerializer(serializers.ModelSerializer):
    comments = CommentModelSerializer(many=True, read_only=True)

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'author', 'created_at', 'comments']


class getAlldataPost(APIView):
    def get(self,request):
        if request.method=="GET" or request.method=="get":
            try:
                post_data=PostModel.objects.all()
                post_serializer=PostModelSerializer(post_data,many=True)
                data=post_serializer.data
                return Response(data)
            except Exception as e:
                err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
                return HttpResponse(json.dumps(err), content_type="application/json")
        else:
            err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
            return HttpResponse(json.dumps(err), content_type="application/json")

class Posttitlenone(APIView):
    def get(self,request):
        if request.method=="GET" or request.method=="get":
            try:
                post_data=PostModel.objects.filter(title=None)
                post_serializer=PostModelSerializer(post_data,many=True)
                data=post_serializer.data
                return Response(data)
            except Exception as e:
                err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
                return HttpResponse(json.dumps(err), content_type="application/json")
        else:
            err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
            return HttpResponse(json.dumps(err), content_type="application/json")
class PostRecentComments(APIView):
    def get(self,request):
        if request.method=="GET" or request.method=="get":
            try:
                posts_with_recent_comments = PostModel.objects.annotate(
                    recent_comment_date=Max('comments__publication_date')
                )

                # Order the posts based on the timestamp of their most recent comment
                posts_with_recent_comments = posts_with_recent_comments.order_by('-recent_comment_date')

                post_serializer=PostModelSerializer(posts_with_recent_comments,many=True)
                data=post_serializer.data
                return Response(data)
            except Exception as e:
                err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
                return HttpResponse(json.dumps(err), content_type="application/json")
        else:
            err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
            return HttpResponse(json.dumps(err), content_type="application/json")

class Postcreatedate(APIView):
    def get(self,request):
        if request.method=="GET" or request.method=="get":
            try:
                posts_ordered_by_creation_date = PostModel.objects.order_by('-created_at')

                post_serializer=PostModelSerializer(posts_ordered_by_creation_date,many=True)
                data=post_serializer.data
                return Response(data)
            except Exception as e:
                err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
                return HttpResponse(json.dumps(err), content_type="application/json")
        else:
            err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
            return HttpResponse(json.dumps(err), content_type="application/json")


class Totalnocomments(APIView):
    def get(self,request):
        if request.method=="GET" or request.method=="get":
            try:
                post_data=PostModel.objects.all()
                data_dict=[]
                for i in post_data:
                    dt_dict={}
                    dt_dict_data=CommentModel.objects.filter(post_id=i.id).count()
                    dt_dict['id']=i.id
                    dt_dict['cmt_count']=dt_dict_data
                    dt_dict['title']=i.title
                    dt_dict['author']=i.author
                    dt_dict['created_at']=str(i.created_at)
                    data_dict.append(dt_dict.copy())
                return HttpResponse(json.dumps({"data":data_dict}),content_type="applicatn/json")

            except Exception as e:
                err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
                return HttpResponse(json.dumps(err), content_type="application/json")
        else:
            err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
            return HttpResponse(json.dumps(err), content_type="application/json")

def generate_sentence():
    while True:
        yield ' '.join([random.choice(['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliqua']) for _ in range(10)]) + '\n'
        time.sleep(1)  # Delay to simulate real-time streaming

@require_http_methods(["GET"])
def stream_sentence(request):
    response = StreamingHttpResponse(generate_sentence(), content_type="text/plain")
    return response


from ailaysapro.celery import count_words_in_file

@csrf_exempt
def readthefiledata_count(request):
    file_d=request.FILES.get('file')
    if file_d==None:
        return HttpResponse(json.dumps({"total_count": 0}), content_type="application/json")
    result = count_words_in_file.delay(file_d)
    return HttpResponse(json.dumps({"total_count":result}),content_type="application/json")