
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from api.models import Book, User
from api.serializers import BookModelSerializer, UserModelSerializer
from rest_framework import viewsets


class BookAPIView(APIView):

    def get(self,request,*args,**kwargs):
        book_id = kwargs.get('id')
        if book_id:
            book = Book.objects.filter(id=book_id,is_delete=False)
            serialize = BookModelSerializer(book,many=True).data
            # print(serialize)
            return Response({
                'status':200,
                "message":"查询一个书籍",
                "result":serialize,
            })
        else:
            books = Book.objects.filter(is_delete=False)
            serialize = BookModelSerializer(books,many=True).data
            return Response({
                'status': 200,
                "message": "查询所有书籍",
                "result": serialize,
            })

    def post(self,request,*args,**kwargs):
        request_data = request.data
        print(request_data)
        if isinstance(request_data,dict):
            many = False
        elif isinstance(request_data,list):
            many = True
        else:
            return Response({
                "status":400,
                "message":"添加失败"
            })
        serialize = BookModelSerializer(data=request_data,many=many)
        serialize.is_valid(raise_exception=True)
        book = serialize.save()
        return Response({
            'status': 200,
            "message": "添加书籍",
            "result": BookModelSerializer(book,many=many).data,
        })


    def delete(self,request,*args,**kwargs):
        id = kwargs.get('id')
        if id:
            # 删除单个
            ids = [id]
        else:
            ids = request.data
        response = Book.objects.filter(id__in=ids,is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status":200,
                "message":"删除成功",
            })
        else:
            return Response({
                "status": 400,
                "message": "删除失败或已被删除",
            })

    # 更新单个整体
    def put(self,request,*args,**kwargs):
        # 获取到修改的值
        request_data = request.data
        # 获取到被修改的对象
        book_id = kwargs.get('id')
        try:
            book_obj = Book.objects.get(id=book_id)
        except:
            return Response({
                "status":400,
                "message":"对象不存在"
            })
        serializer = BookModelSerializer(data=request_data,instance=book_obj,partial=True)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        return Response({
            "status":200,
            "message":"修改成功",
            "result":BookModelSerializer(book).data
        })

    # def patch(self,request,*args,**kwargs):
    #     # 获取到修改的值
    #     request_data = request.data
    #     # 获取到被修改的对象
    #     book_id = kwargs.get('id')
    #     try:
    #         book_obj = Book.objects.get(id=book_id)
    #     except:
    #         return Response({
    #             "status": 400,
    #             "message": "对象不存在"
    #         })
    #     serializer = BookModelSerializer(data=request_data, instance=book_obj,partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     book = serializer.save()
    #     return Response({
    #         "status": 200,
    #         "message": "修改成功",
    #         "result": BookModelSerializer(book).data
    #     })

    def patch(self,request,*args,**kwargs):
        '''
        更新单个  id   kwargs.get('id')
        更新多个  [{},{},{}]
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        book_id = kwargs.get('id')
        request_data = request.data
        # 修改单个
        if book_id and isinstance(request_data,dict):
           ids = [book_id]
           request_data = [request_data]
        elif not book_id and isinstance(request_data,list):
           ids = []
           for i in request_data:
               id = i.pop('id',None)
               if id:
                   ids.append(id)
               else:
                   return Response({
                       'status':400,
                        "message":"id不存在"
                        })
        else:
           return Response({
               "status":400,
               "message":"格式错误"
           })

        books_obj = []
        new_data = []
        for index,id in enumerate(ids):
            print(index,id)
            try:
                book_obj = Book.objects.get(id)
                print(book_obj)
                books_obj.append(book_obj)
                new_data.append(request_data[index])
            except:
                continue

        serializer = BookModelSerializer(data=new_data,instance=books_obj,partial=True,many=True)
        serializer.is_valid(raise_exception=True)
        datas = serializer.save()
        return Response({
            "status":200,
            "message":"成功",
            "result": BookModelSerializer(datas).data
        })

class BookGenericAPIView(GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         ):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    def get(self,request,*args,**kwargs):
        if "id" in kwargs:
            return self.retrieve(request,*args,**kwargs)

        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)

class BookGenerics(generics.ListAPIView,
                   generics.ListCreateAPIView):
    queryset = Book.objects.filter()
    serializer_class = BookModelSerializer
    lookup_field = "id"

class UserAPIView(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = "id"

    def register(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def login(self,request,*args,**kwargs):
        request_data = request.data
        print(request_data)

        user= User.objects.filter(username=request_data.get('username'),password=request_data.get('password'))
        if user:
            return Response({
                "status":200,
                "message":"登陆成功"
            })
        return Response({
            "status":400,
            "message":"登陆失败"
        })

