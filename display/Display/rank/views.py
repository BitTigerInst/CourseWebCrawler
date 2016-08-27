#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import pymongo
# Create your views here.

dbName = 'imooc_class_central'
client = pymongo.MongoClient('localhost', 27017)
db = client[dbName]
courses = db['courses']

def rank(request):
	sortname = request.GET.get('sort', 'score')
	if sortname == 'score':
		secondsort = "review_num"
	else:
		secondsort = "score"
	ImoocList = courses.find({"platform":"imooc"}).sort([(sortname, -1),(secondsort, -1)]).limit(10)
	ClassCentralList = courses.find({"platform":{"$ne":"imooc"}}).sort([(sortname, -1),(secondsort, -1)]).limit(10)
	return render(request, 'rank.html', {'ImoocList':ImoocList, 'ClassCentralList':ClassCentralList})


