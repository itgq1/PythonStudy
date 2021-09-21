from django.shortcuts import render, redirect
from app01 import models

# Create your views here.
def add_publisher(request):
    if request.method == 'POST':
        # 获取表单提交的信息
        publisher_name = request.POST.get("name")
        publisher_address = request.POST.get("address")
        # 保存到数据库
        models.Publisher.objects.create(name=publisher_name, address=publisher_address)
        return redirect('/app01/publisher_list')

    return render(request, "add_publisher.html")

def publisher_list(request):
    return render(request, "publisher_list.html")