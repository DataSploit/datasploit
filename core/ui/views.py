from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from osint import *

from celery import group

import re, json
from uuid import uuid4
from pymongo import MongoClient
from bson import json_util
from json2html import *
import cgi
import config
# Create your views here.

def index(request):
	return render(request, 'index.html')

def search(request):
	if request.method == "POST":
		domain = request.POST.get("domain", None)
		if domain:
			domain = domain.lower()
			pattern = "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"
			check = re.match(pattern, domain)
			if check:
				functions = [domain_GooglePDF.run]	
				functions = [domain_GooglePDF.run, domain_checkpunkspider.checkpunkspider, domain_dnsrecords.parse_dns_records, domain_emailhunter.emailhunter, domain_forumsearch.boardsearch_forumsearch, domain_github.github_search, domain_history.netcraft_domain_history, domain_pagelinks.pagelinks, domain_shodan.shodandomainsearch, domain_sslinfo.check_ssl_htbsecurity, domain_wappalyzer.wappalyzeit, domain_whois.whoisnew, domain_wikileaks.wikileaks, domain_subdomains.run]	
				
				taskId = str(uuid4())
				client = MongoClient()
			        db = client.database1
			        d = {"status_check": taskId, "count": len(functions), "type": "poller"}
				print d
			        result = db.domaindata.insert(d, check_keys=False)
				g = group(i.s(domain, taskId) for i in functions)
				res = g()
				#for fn in functions:
				#	print fn
				#	fn.delay(domain, taskId)
				#print domain_whois.whoisnew.delay(domain)
				return render(request, 'search.html', {"domain": domain, "taskId": taskId}) 
			else:
				return redirect('osint:index')
		return HttpResponse("Search")
	else:
		return redirect('osint:index')

@csrf_exempt
def status(request):
	if request.method == "POST":
		taskId = request.POST.get("taskId", None)
		domain = request.POST.get("domain", None)
		if taskId and domain:
			client = MongoClient(config.mongo_uri)
                        db = client.database1
			cursor = db.domaindata.find({"type": "poller", "status_check": taskId})
			if cursor.count() == 1:
				doc = cursor.next()
				cursor = db.domaindata.find({"targetname": domain, "taskId": taskId})
				if cursor.count() == doc['count']:
					scanned = []
					try:
                                                while True:
                                                        doc = cursor.next()
							rec = doc['record']
							print rec['type']
							if rec['type'] == "Google Search":
								html = "<ul class='collection'>"
								for i, j in rec['data'].iteritems():
									html += "<li class='collection-item'><b>%s</b>" % str(i).upper()
									html += "<ul class='collection'>"
									if isinstance(j, list):
										for x in j:
											html += "<li class='collection-item'>%s</li>" % x
									else:
										html += "<li class='collection-item'>%s</li>" % j
									html += "</li></ul>"
								html += "</ul>"
								rec['data'] = html
							elif rec['type'] == "DNS Records":
								html = "<ul class='collection'>"
								for i, j in rec['data'].iteritems():
									html += "<li class='collection-item'><b>%s</b>" % i
									html += "<ul class='collection'>"
									if isinstance(j, list):
										for x in j:
											html += "<li class='collection-item'>%s</li>" % x
									else:
										html += "<li class='collection-item'>%s</li>" % j
									html += "</li></ul>"
								html += "</ul>"
								rec['data'] = html
							elif rec['type'] == "Page Links":
								html = "<ul class='collection'>"
								for i in rec['data']:
									html += "<li class='collection-item'><a href='%s'>%s</a></li>" % (cgi.escape(i), cgi.escape(i))
								html += "</ul>"		
								rec['data'] = html
							elif rec['type'] == "Domain History":
								if rec['data']:
									html = "<ul class='collection'>"
									for i, j in rec['data'].iteritems():
										html += "<li class='collection-item'><b>%s</b><br>%s</li>" % (i, j)
									html += "</ul>"
									rec['data'] = html
								else:
									rec['data'] = "<p>No information found</p>"
							elif rec['type'] == "GitHub Results":
								html = "<p>%s</p>" % ("No information found" if not rec['data'] else rec['data'][0])
								rec['data'] = html
							elif rec['type'] == "Forum Search":
								html = "<ul class='collection'>"
								for i, j in rec['data'].iteritems():
									html += "<li class='collection-item'><b>%s</b><br><a href='%s'>%s</a></li>" % (i, j, j)
								html += "</ul>"
                                                                rec['data'] = html
							elif rec['type'] == "WikiLeaks":
								if rec['data']:
									html = "<ul class='collection'>"
									for i, j in rec['data'].iteritems():
										html += "<li class='collection-item'><b>%s</b><br><a href='%s'>%s</a></li>" % (i, j, j)
									html += "</ul>"
									rec['data'] = html
								else:
                                                                        rec['data'] = "<p>No information found</p>"
							elif rec['type'] == "Email Hunter":
								html = "<ul class='collection'>"
								for i in rec['data']:
                                                                        html += "<li class='collection-item'><a href='mailto:%s'>%s</a></li>" % (i, i)
								html += "</ul>"
                                                                rec['data'] = html
							elif rec['type'] == "WHOIS Information":
								if rec['data']:
									html = json2html.convert(json = json.loads(json.dumps(rec['data'], default=json_util.default)))
									rec['data'] = html
								else:
									rec['data'] = "<p>No information found</p>"
							elif rec['type'] == "PunkSpider":
								if rec['data']['data']:
									html = json2html.convert(json = rec['data'])
									rec['data'] = html
								else:
									rec['data'] = "<p>No information found</p>"
							elif rec['type'] == "Shodan":
								if rec['data']['matches']:
									html = json2html.convert(json = rec['data'])
									rec['data'] = html
								else:
									rec['data'] = "<p>No information found</p>"
							elif rec['type'] == "SSL Information":
								html = json2html.convert(json = rec['data'])
								rec['data'] = html
							elif rec['type'] == "Subdomains":
								if rec['data']:
									html = "<ul class='collection'>"
									for i in rec['data']:
										html += "<li class='collection-item'><a href='http://%s'>%s</a></li>" % (i, i)
									html += "</ul>"
								else:
									html = "<p>No Information found</p>"
                                                                rec['data'] = html
							elif rec['type'] == "WapAlyzer":
								if rec['data']:
									html = "<ul class='collection'>"
									for i in rec['data']:
										html += "<li class='collection-item'>%s</li>" % i
									html += "</ul>"
								else:
									html = "<p>No Information found</p>"
                                                                rec['data'] = html
							else:
								html = json.dumps(rec['data'], default=json_util.default)
								rec['data'] = html
							doc['record'] = rec
                                                        scanned.append(doc['record'])
					except:
						pass
						
					d = {"status": True, "message": scanned}
					j = json.dumps(d, default=json_util.default)
					return HttpResponse(j)
				else:
					scanned = ['']
					try:
						while True:
							doc = cursor.next()
							scanned.append(doc['record']['type'])
					except:
						pass
					d = {"status": False, "message": scanned}
					j = json.dumps(d)
					return HttpResponse(j)
			else:
				d = {"status": False, "message": "STOP"}
                                j = json.dumps(d)
                                return HttpResponse(j)
		else:
			return redirect('osint:index')
	else:
		return redirect('osint:index')












