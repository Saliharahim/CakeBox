from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from cakeApp.models import Cakes
from rest_framework import serializers
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions


# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

       




class CakeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Cakes
        fields="__all__"
        # exclude=("id",)


class CakesView(ModelViewSet):
    serializer_class=CakeSerializer
    queryset=Cakes.objects.all()
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=CakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    def get_queryset(self):
        return Cakes.objects.filter(user=self.request.user)







class UserView(ModelViewSet):
    serializer_class=UserSerializer
    model=User
    queryset=User.objects.all()


# class CakeView(ViewSet):

#     def list(self,request,*args,**kw):
#         qs=Cakes.objects.all()
#         if "flavour" in request.query_params:
#             flav=request.query_params.get("flavour")
#             qs=qs.filter(flavour__iexact=flav)

#         if "tier" in request.query_params:
#             tr=request.query_params.get("tier")
#             qs=qs.filter(tier__iexact=tr)

#         if "price_gt" in request.query_params:
#             pr=request.query_params.get("price_gt")
#             qs=qs.filter(price__gte=pr)

#         serializer=CakeSerializer(qs,many=True)
#         return Response(data=serializer.data)
    
#     def create(self,request,*args,**kw):
#         serializer=CakeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         return Response(data=serializer.errors)
    

#     def retrieve(self,request,*args,**kw):
#         id=kw.get("pk")
#         qs=Cakes.objects.get(id=id)
#         serializer=CakeSerializer(qs)
#         return Response(data=serializer.data)
    
    
#     def update(self,request,*args,**kw):
#         id=kw.get("pk")
#         cake_obj=Cakes.objects.get(id=id)
#         serializer=CakeSerializer(instance=cake_obj,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         return Response(data=serializer.errors)
    
#     def destroy(self,request,*args,**kw):
#         id=kw.get("pk")
#         try:
#             Cakes.objects.get(id=id)
#             return Response(data="deleted")
#         except Exception:

#             return Response(data="no matching record found")
#     @action(methods=["get"],detail=False)   
#     def weight(self,request,*args,**kw):
#         qs=Cakes.objects.all().values_list("weight",flat=True).distinct()
        # return Response(data=qs)

