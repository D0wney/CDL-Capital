#!/usr/bin/python

import cgi, datetime, sys, LINK_HEADERS
import simplejson as json
sys.path.insert(0, str(LINK_HEADERS.DAO_LINK))
sys.path.insert(0, str(LINK_HEADERS.MODELS_LINK))
sys.path.insert(0, str(LINK_HEADERS.SCRIPTS_LINK))
from company_dao import Company_dao
import quick_sort_companyinfo

print "Content-Type: text/html\r\n\r\n"

cdao = Company_dao()



def main():

    result = cdao.get_all_companies_model()
    #quick_sort_companyinfo.quick_sort_percentchange(result, 0, len(result)-1, "PercentChange")
    #result.sort(key=lambda x: x.get_percent_change(), reverse=True)


    json_object=[]
	
    for i in range(0, 5): #gets top 5 best changes
	json_object.append({"symbol": result[i].get_symbol(), "PercentChange" : result[i].get_percent_change()})

    for i in range(len(result)-1, len(result)-6, -1): #gets top 5 worst changes
	json_object.append({"symbol": result[i].get_symbol(), "PercentChange" : result[i].get_percent_change()})

    json_object.append(len(result))
    json_result = json.dumps(json_object)
    print json_result

main()
