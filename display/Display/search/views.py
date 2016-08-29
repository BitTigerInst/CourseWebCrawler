
#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import json
# Create your views here.

dbName = 'imooc_class_central'
client = pymongo.MongoClient('localhost', 27017)
db = client[dbName]
courses = db['courses']
CourseList = courses.find()
file = open("./search/keyword.txt", 'r')
lines = file.readlines()
CourseNameList = [line.lower().strip() for line in lines]        
#for item in CourseList:
#	CourseNameList.append(item["name"])

def initial(request):
	return render(request, 'result.html', {'CourseNameList':CourseNameList})

def search(request):
	searchname = request.GET.get('coursename', '')
	if searchname == '':
		ImoocSearchList = []
		ClassCentralSearchList = []
	else:
		searchname = eval("\"" + searchname + "\"")
		ImoocSearchList = courses.find({"platform":"imooc", "name":{"$regex":searchname, "$options":"$i"}})
		ClassCentralSearchList = courses.find({"platform":{"$ne":"imooc"}, "name":{"$regex":searchname, "$options":"$i"}})
	return render(request, 'result.html', {'CourseNameList':json.dumps(CourseNameList), 'ImoocSearchList':ImoocSearchList, 'ClassCentralSearchList':ClassCentralSearchList})

