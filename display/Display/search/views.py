#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import pymongo
# Create your views here.

dbName = 'imooc_class_central'
client = pymongo.MongoClient('123.56.12.211', 27017)
db = client[dbName]
courses = db['courses']
ImoocCourseList = courses.find({"platform":"imooc"})
ClassCentralCourseList = courses.find({"platform":{"$ne":"imooc"}})
CourseNameList = ["aaa"]
for item in ImoocCourseList:
	CourseNameList.append(item["name"])
for item in ClassCentralCourseList:
	CourseNameList.append(item["name"])

def initial(request):
	return render(request, 'result.html', {'CourseNameList':CourseNameList})

def search(request):
	searchname = request.GET.get('coursename')
	ImoocSearchList = courses.find({"platform":"imooc", "name":searchname})
	ClassCentralSearchList = courses.find({"platform":{"$ne":"imooc"}, "name":searchname})
	return render(request, 'result.html', {'CourseNameList':CourseNameList, 'ImoocSearchList':ImoocSearchList, 'ClassCentralSearchList':ClassCentralSearchList})

