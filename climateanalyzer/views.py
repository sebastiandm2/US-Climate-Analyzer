from django.shortcuts import render
from .models import President, City, Belongsto, Country
from django.http import HttpResponse
from django.db import connection

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
    _dtBottom = '1950-01-01'
    _dtTop = '2010-01-01'
    
    query = """
    with bro as
    (select avg(averagetemperature) as avvg, extract(year from dt) as yr 
    from country
    where dt >= to_date(%0s, \'YYYY-DD-MM\') and dt < to_date(%1s, \'YYYY-DD-MM\')
    group by extract(year from dt))
    select 1 as id, avvg, yr from bro order by avvg desc fetch first 1 rows only
    """

    #returns list w only 1 value
    cursor = connection.cursor()
    cursor.execute(query, [_dtBottom, _dtTop])
    result = cursor.fetchall()
    cursor.close()
    a = result[0] #tuple

    #returns list w multiple values NEED TO FINISH
    dtLow = str(a[2]) + '-01-01' #year is in the 2nd element of the tuple
    dtHigh = str(a[2]) + '-31-12'
    query = """
    select * from president where (term_start <= to_date(%0s, \'YYYY-DD-MM\')) and (term_end >= to_date(%1s, \'YYYY-DD-MM\'))
    """
    cursor = connection.cursor()
    cursor.execute(query, [dtLow, dtHigh])
    result = cursor.fetchall()
    cursor.close()
    
    for p in result:
        print(p[0],',' ,p[3])

    temperature = a[1]
    print('The year was', a[2], 'and the temperature was', round(a[1], 2))

    return HttpResponse("findMaxPres successful")

#find which party on average displays the highest temperatures
def findParty(request):
    query = """
    select party, avg(averagetemperature) as avg from president, country
    where dt < term_end and dt > term_start
    group by party
    """

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    for p in result:
        print('The average for the', p[0], 'party is', round(p[1], 2))

    return HttpResponse("findParty successful")

#given a year, return the city that had the highest average temperature that year. Display city, state and temperature
def findCity(request):
    #parameters
    yr = '2000'
    _dtBottom = yr + '-01-01'
    _dtTop = yr + '-31-12'

    query = """
    select avg(averagetemperature) as avg, city from city 
    where dt >= to_date(%0s, \'YYYY-DD-MM\') and dt <= to_date(%1s, \'YYYY-DD-MM\')
    group by city
    order by avg desc
    fetch first 1 rows only
    """

    cursor = connection.cursor()
    cursor.execute(query, [_dtBottom, _dtTop])
    result = cursor.fetchall()
    cursor.close()

    row = result[0]
    city = row[1]
    temperature = round(row[0], 2)

    query = """
    select distinct city.city, state 
    from city inner join belongsto on city.city = belongsto.city where city.city = %s
    """

    cursor = connection.cursor()
    cursor.execute(query, [city])
    result = cursor.fetchall()
    cursor.close()

    row = result[0]
    state = row[1]

    print(city, ',', state, 'has the highest average temperture in the year', yr, 'of', temperature)

    return HttpResponse("findCity successful")

#given a city, find the year that had the highest average temperature. Display city, state, year, and temperature
def findYear(request):
    #parameters
    city = 'Miami'

    query = """
    select extract(year from dt), avg(averagetemperature)
    from city
    where city.city = %s and averagetemperature is not null
    group by extract(year from dt)
    order by avg(averagetemperature) desc
    fetch first 1 rows only
    """

    cursor = connection.cursor()
    cursor.execute(query, [city])
    result = cursor.fetchall()
    cursor.close()

    row = result[0]
    yr = row[0]
    temperature = round(row[1], 2)

    query = """
    select distinct city.city, state 
    from city inner join belongsto on city.city = belongsto.city where city.city = %s
    """

    cursor = connection.cursor()
    cursor.execute(query, [city])
    result = cursor.fetchall()
    cursor.close()

    row = result[0]
    state = row[1]

    print(city, ',', state, 'had the highest average temperture of', temperature, 'in the year', yr)

    return HttpResponse("findCity successful")