import datetime
import json,re

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from userapp.models import UserProfile
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
class UserappSerializer(serializers.Serializer):
    class meta:
        model=UserProfile
        fields = '__all__'
def HandlePagination(pagenum,page_size,data):
    has_next=False
    hax_pre=False
    current_page=pagenum+1
    if len(data)<=page_size and pagenum==1:
        has_next=False
        hax_pre=False
    elif len(data)<=page_size and pagenum!=1:
        has_next=False
        hax_pre=True
    elif len(data)>=page_size and pagenum!=1:
        has_next=True
        hax_pre=True

    else:
        has_next=False
        hax_pre=False
    return {"next":has_next,"pre":hax_pre,"current":current_page}



@csrf_exempt
def createuser_profile(request):
    if request.method=='POST' or request.method=='post':
        try:
            create_data=json.loads(request.POST.get('data'))

            if create_data.get("email")==None or create_data.get("email")=="" or create_data.get("email")=="":
                raise Exception("INVALID EMAIL")

            if create_data.get("name")==None or create_data.get("name")=="" or create_data.get("name")=="":
                raise Exception("INVALID NAME")
            if create_data.get("dob")==None or create_data.get("dob")=="" or create_data.get("dob")=="":
                raise Exception("INVALID DOB")
            if create_data.get("contactnumber")==None or create_data.get("contactnumber")=="" or create_data.get("contactnumber")=="":
                raise Exception("INVALID CONTACT NUMBER")
            if create_data.get("address")==None or create_data.get("address")=="" or create_data.get("address")=="":
                raise Exception("INVALID ADDRESS")
            if create_data.get("gender")==None or create_data.get("gender")=="" or create_data.get("gender")=="":
                raise Exception("INVALID GENDER")
            if create_data.get("usercode")==None or create_data.get("usercode")=="" or create_data.get("usercode")=="":
                raise Exception("INVALID USER CODE")
            if create_data.get("userpassword")==None or create_data.get("userpassword")=="" or create_data.get("userpassword")=="":
                raise Exception("INVALID USER PASSWORD")
            if request.FILES.get("file")==None:
                raise Exception("INVALID PROFILE")
            pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
            email = create_data.get("email", None)
            if re.match(pattern, email) == False:
                raise Exception("Invalid Mail Format")
            with transaction.atomic():
                user_account_create=user = User.objects.create_user(username=create_data.get("usercode"), email=email, password=create_data.get("userpassword"))
                user_creation=UserProfile.objects.create(
                    user_id=user_account_create.id,
                    name=create_data.get("name"),
                    email=email,
                    dob=str(create_data.get("dob")),
                    contactnumber=create_data.get("contactnumber"),
                    address=create_data.get("address"),
                    gender=create_data.get("gender"),
                    profile_picture=request.FILES.get("file"),
                    lastlogin=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
            success={"status":"sucesss","message":"User Created Successfully"}
            return HttpResponse(json.dumps(success),content_type="application/json")

        except Exception as e:
            err={"err_code":"INVALID_DATA","err_desc":str(e),"err_line":str(e.__traceback__.tb_lineno)}
            return HttpResponse(json.dumps(err),content_type="application/json")


    elif request.method=='GET' or request.method=='GET':
        try:
            page_num=int(request.GET.get('page',1))
            page_size=int(request.GET.get('pagesize',10))
            start_index=(page_num-1)*page_size
            end_index=((page_num)*page_size) +1
            con=Q()
            if "name" in request.GET and request.GET.get("name")!=None and request.GET.get("name")!="" and request.GET.get("name")!="0":
                con &=Q(name__icontains=request.GET.get("name"))
            if "email" in request.GET and request.GET.get("email")!=None and request.GET.get("email")!="" and request.GET.get("email")!="0":
                con &=Q(email__icontains=request.GET.get("email"))

            if "contactnumber" in request.GET and request.GET.get("contactnumber")!=None and request.GET.get("contactnumber")!="" and request.GET.get("contactnumber")!="0":
                con &=Q(contactnumber__icontains=request.GET.get("contactnumber"))
            data_list_count=UserProfile.objects.filter(con).count()
            data_list=UserProfile.objects.filter(con)[start_index:end_index]
            data_output_list=[]
            for i in data_list:
                data_dict={}
                data_dict['user']={"username":str(i.user.username),"user_id":str(i.user_id),"user_email":str(i.user.email)}
                data_dict['name']=str(i.name)
                data_dict['email']=str(i.email)
                data_dict['dob']=str(i.dob)
                data_dict['contactnumber']=str(i.contactnumber)
                data_dict['address']=str(i.address)
                if i.gender==1 or i.gender=='1':
                    data_dict['gender']='Male'
                elif i.gender==2 or i.gender=='2':
                    data_dict['gender']='FeMale'
                else:
                    data_dict['gender'] = 'Others'
                data_dict['profile_picture']=str("")+str(i.profile_picture)
                data_dict['lastlogin']=str(i.lastlogin)
                data_dict['id']=str(i.id)
                data_output_list.append(data_dict.copy())
            pagination=HandlePagination(page_num,page_size,data_list)
            output_data={"data":data_output_list,"pagination":pagination}
            return HttpResponse(json.dumps(output_data),content_type="application/json")

        except Exception as e:
            err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
            return HttpResponse(json.dumps(err), content_type="application/json")

    else:
        err={"err_code":"INVALID_CODE","err_desc":str(request.method)+" METHOD NOT ALLOWED"}
        return HttpResponse(json.dumps(err),content_type="application/json")

@csrf_exempt
def profileImageView(request,id):
    if request.method=='GET' or request.method=='get':
        try:
            data=UserProfile.objects.get(id=id)
            filename_a=str(data.profile_picture).split("/")
            filename_type=filename_a[-1].split(".")[-1]
            print(filename_type)
            resp= HttpResponse(data.profile_picture,content_type="image/"+str(filename_type))
            resp['Content-Disposition']="attachment;filename="+str(filename_a[-1])
            return resp
        except Exception as e:
            err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
            return HttpResponse(json.dumps(err), content_type="application/json")
    else:
        err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
        return HttpResponse(json.dumps(err), content_type="application/json")

def userprofileupdate(request):
    try:
        create_data = json.loads(request.POST.get('data'))

        if create_data.get("email") == None or create_data.get("email") == "" or create_data.get("email") == "":
            raise Exception("INVALID EMAIL")

        if create_data.get("name") == None or create_data.get("name") == "" or create_data.get("name") == "":
            raise Exception("INVALID NAME")
        if create_data.get("dob") == None or create_data.get("dob") == "" or create_data.get("dob") == "":
            raise Exception("INVALID DOB")
        if create_data.get("contactnumber") == None or create_data.get("contactnumber") == "" or create_data.get(
                "contactnumber") == "":
            raise Exception("INVALID CONTACT NUMBER")
        if create_data.get("address") == None or create_data.get("address") == "" or create_data.get("address") == "":
            raise Exception("INVALID ADDRESS")
        if create_data.get("gender") == None or create_data.get("gender") == "" or create_data.get("gender") == "":
            raise Exception("INVALID GENDER")
        if create_data.get("usercode") == None or create_data.get("usercode") == "" or create_data.get(
                "usercode") == "":
            raise Exception("INVALID USER CODE")
        if create_data.get("userpassword") == None or create_data.get("userpassword") == "" or create_data.get(
                "userpassword") == "":
            raise Exception("INVALID USER PASSWORD")
        if request.FILES.get("file") == None:
            raise Exception("INVALID PROFILE")
        pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        email = create_data.get("email", None)
        if re.match(pattern, email) == False:
            raise Exception("Invalid Mail Format")
        with transaction.atomic():
            user_account_create = user = User.objects.filter(id=create_data.get("user_id")).update(username=create_data.get("usercode"), email=email
                                                                  )
            user_creation = UserProfile.objects.filter(id=create_data.get('id')).update(

                name=create_data.get("name"),
                email=email,
                dob=str(create_data.get("dob")),
                contactnumber=create_data.get("contactnumber"),
                address=create_data.get("address"),
                gender=create_data.get("gender"),
                profile_picture=request.FILES.get("file"),
                lastlogin=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
        success = {"status": "sucesss", "message": "User Created Successfully"}
        return HttpResponse(json.dumps(success), content_type="application/json")

    except Exception as e:
        err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
        return HttpResponse(json.dumps(err), content_type="application/json")

@csrf_exempt
def ProfileDelete(request):
    if request.method=='post' or request.method=='POST':
        try:
            with transaction.atomic():
                data=json.loads(request.body)
                if data.get("id")==None or data.get("id")=="" or data.get("id")=="0":
                    raise  Exception("INVALID USER ID")
                data_get=UserProfile.objects.filter(id=data.get("id"))
                if len(data_get)==0:
                    raise  Exception("INVALID USER ID. RECORDS NOT AVAILABLE")

                data_user_id=data_get[0].user_id
                data_get.delete()
                User.objects.filter(id=data_user_id).delete()
            success = {"status": "sucesss", "message": "User Deleted Successfully"}
            return HttpResponse(json.dumps(success), content_type="application/json")
        except Exception as e:
            err = {"err_code": "INVALID_DATA", "err_desc": str(e), "err_line": str(e.__traceback__.tb_lineno)}
            return HttpResponse(json.dumps(err), content_type="application/json")
    else:
        err = {"err_code": "INVALID_CODE", "err_desc": str(request.method) + " METHOD NOT ALLOWED"}
        return HttpResponse(json.dumps(err), content_type="application/json")