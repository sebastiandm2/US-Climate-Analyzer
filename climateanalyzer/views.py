from django.shortcuts import render
from .models import President, City, Belongsto, Country
from django.http import HttpResponse

# Create your views here.

#given a range of time (dtBottom, dtTop), return the city with the lowest average temperature. Display city, state, date, temp
def findMinTempCity(request):
    #parameters
    _dtBottom = '2000-01-01'
    _dtTop = '2010-01-01'
    
    #returns list w only 1 value
    result = City.objects.raw('select * from city where averagetemperature = (select min(averagetemperature) as averagetemperature from city where dt >= to_date(%0s, \'YYYY-DD-MM\') and dt < to_date(%1s, \'YYYY-DD-MM\'));', [_dtBottom, _dtTop]) #returns list w only 1 value
    a = result[0]

    #returns list w only 1 value
    result = Belongsto.objects.raw('select * from belongsto where city = %s;', [a.city]) 
    b = result[0]

    #return values?
    print(a.city, b.state, a.dt, a.averagetemperature)

    return HttpResponse("findMinTempCity successful")

#given a range of time (dtBottom, dtTop), return the city with the highest average temperature. Display city, state, date, temp
def findMaxTempCity(request):
    #parameters
    _dtBottom = '2000-01-01'
    _dtTop = '2010-01-01'
    
    #returns list w only 1 value
    result = City.objects.raw('select * from city where averagetemperature = (select max(averagetemperature) as averagetemperature from city where dt >= to_date(%0s, \'YYYY-DD-MM\') and dt < to_date(%1s, \'YYYY-DD-MM\'));', [_dtBottom, _dtTop]) #returns list w only 1 value
    a = result[0]

    #returns list w only 1 value
    result = Belongsto.objects.raw('select 1 as id, state from belongsto where city = %s;', [a.city]) 
    b = result[0]

    #return values?
    print(a.city, b.state, a.dt, a.averagetemperature)

    return HttpResponse("findMaxTempCity successful")

#return the president with the lowest average temperature. Display name, party, termstart, termend
def findMaxPres(request):
    #parameters
    _dtBottom = '2000-01-01'
    _dtTop = '2010-01-01'
    
    #returns list w only 1 value
    result = Country.objects.raw('with bro as (select avg(averagetemperature) as avvg, extract(year from dt) as yr from country where dt >= to_date(%0s, \'YYYY-DD-MM\') and dt < to_date(%1s, \'YYYY-DD-MM\') group by extract(year from dt)) select 1 as id, avvg, yr from bro order by avvg desc fetch first 1 rows only;', [_dtBottom, _dtTop]) #returns list w only 1 value
    a = result[0]

    #returns list w multiple values NEED TO FINISH
    yr = str(a.yr) + '-01-01'
    result = President.objects.raw('select * from president where (term_start <= to_date(%s, \'YYYY-DD-MM\')) and (term_end >= to_date(%s, \'YYYY-DD-MM\'));', [yr]) 
    
    

    return HttpResponse("findMaxPres successful")