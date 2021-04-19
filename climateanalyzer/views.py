from django.shortcuts import render
from .models import President, City, Belongsto, Country, State
from django.http import HttpResponse
from django.db import connection
from .utils import getScatterPlot1, getScatterPlot2, getBarPlot, getBarPlot2, getBarPlot3

from django.views import View

def mainView(request):
    city = 'Boston'
    state = 'Florida'
    country = 'United States'
    yrBottom = '1950'
    yrTop = '2000'
    dtBottom = '1900-01-01'
    dtTop = '2010-01-01'
    president = 'Bill Jefferson Clinton'
    
    table = 'city' #request.POST['table']
    query = 'yearlyAvg' #request.POST['query']



    #City------------------------------------------------------------------------------------------------------------------------------------------------
    #Yearly Average
    qs = CityYearlyAvg(city, yrBottom, yrTop)
    x = [float(r[0]) for r in qs]
    z = [r[1] for r in qs]
    y = [float(r[2]) for r in qs]
    chart = getScatterPlot1(x, y, z, city, yrBottom, yrTop)

    #Daily Pres
    qs = CityDailyPres(city, president)
    x = [r[0]for r in qs]
    y = [float(r[1]) for r in qs]
    chart = getScatterPlot2(x, y, president, city)

    #Party
    qs = CityParty(city, dtBottom, dtTop)
    x = [r[0] for r in qs]
    y = [r[1] for r in qs]
    chart = getBarPlot(x, y, city, dtBottom, dtTop)

    #Avg Pres
    qs = CityAvgPres(city)
    x = [r[0] for r in qs]
    y = [r[1] for r in qs]
    chart = getBarPlot2(x, y, city)

    #State----------------------------------------------------------------------------------------------------------------
    #Yearly Average
    qs = StateYearlyAvg(state, yrBottom, yrTop)
    x = [float(r[0]) for r in qs]
    z = [r[1] for r in qs]
    y = [float(r[2]) for r in qs]
    chart = getScatterPlot1(x, y, z, state, yrBottom, yrTop)

    #Daily Pres
    qs = StateDailyPres(state, president)
    x = [r[0]for r in qs]
    y = [float(r[1]) for r in qs]
    chart = getScatterPlot2(x, y, president, state)

    #Party
    qs = StateParty(state, dtBottom, dtTop)
    x = [r[0] for r in qs]
    y = [r[1] for r in qs]
    chart = getBarPlot(x, y, state, dtBottom, dtTop)

    #Avg Pres
    qs = StateAvgPres(state)
    x = [r[0] for r in qs]
    y = [r[1] for r in qs]
    chart = getBarPlot2(x, y, state)
    
    #Country-------------------------------------------------------------------------------------------------------------------------------------------
    #Yearly Average
    qs = CountryYearlyAvg(country, yrBottom, yrTop)
    x = [float(r[0]) for r in qs]
    z = [r[1] for r in qs]
    y = [float(r[2]) for r in qs]
    chart = getScatterPlot1(x, y, z, country, yrBottom, yrTop)

    #Max
    qs = CountryMaxPres(country)
    x = [r[0] for r in qs]
    y = [r[1] for r in qs]
    chart2 = getBarPlot3(x, y)

    #Party
    qs = CountryParty(country, dtBottom, dtTop)
    x = [r[0] for r in qs]
    y = [r[1] for r in qs]
    chart = getBarPlot(x, y, country, dtBottom, dtTop)

    #Avg Pres
    qs = CountryAvgPres(country)
    x = [r[0] for r in qs]
    y = [r[1] for r in qs]
    chart= getBarPlot2(x, y, country)

    return render(request, 'climate/main.html', {'chart': chart2})

#City
def CityYearlyAvg(city, yrBottom, yrTop):
    query = """
    with temp as (select city, extract(year from dt) as yr, avg(averagetemperature) as yearlyavg from city
    group by extract(year from dt), city.city)
    select yr as year, president_name as president, yearlyavg from temp, president
    where yr <= extract(year from term_end) and yr >= extract(year from term_start) 
    and yr <= %0s and yr >= %1s
    and city = %2s
    order by year
    """

    cursor = connection.cursor()
    cursor.execute(query, [yrTop, yrBottom, city])
    result = cursor.fetchall()
    cursor.close()
    return result

def CityDailyPres(city, president):
    query = """
    with temp as (select term_start as s, term_end as e from president where president_name = %0s)
    select dt, averagetemperature from temp, city
    where dt >= s and dt <= e
    and city = %1s
    order by dt asc
    """

    cursor = connection.cursor()
    cursor.execute(query, [president, city])
    result = cursor.fetchall()
    cursor.close()
    return result

def CityParty(city, dtBottom, dtTop):
    query = """
    select party, avg(averagetemperature) from president, city
    where dt < term_end and dt > term_start
    and dt >= to_date(%0s, \'YYYY-MM-DD\') and dt <= to_date(%1s, \'YYYY-MM-DD\')
    and city = %2s
    group by party
    """

    cursor = connection.cursor()
    cursor.execute(query, [dtBottom, dtTop, city])
    result = cursor.fetchall()
    cursor.close()
    return result

def CityAvgPres(city):
    query = """
    with temp as (select president_name, avg(averagetemperature) as avg from city, president
    where dt < term_end and dt > term_start
    and city = %0s
    group by president_name)
    select president.president_name, temp.avg from temp, president
    where temp.president_name = president.president_name
    order by term_start asc
    """

    cursor = connection.cursor()
    cursor.execute(query, [city])
    result = cursor.fetchall()
    cursor.close()
    return result

#State
def StateYearlyAvg(state, yrBottom, yrTop):
    query = """
    with temp as (select state, extract(year from dt) as yr, avg(averagetemperature) as yearlyavg from state
    group by extract(year from dt), state.state)
    select yr as year, president_name as president, yearlyavg from temp, president
    where yr <= extract(year from term_end) and yr >= extract(year from term_start) 
    and yr <= %0s and yr >= %1s
    and state = %2s
    order by year
    """

    cursor = connection.cursor()
    cursor.execute(query, [yrTop, yrBottom, state])
    result = cursor.fetchall()
    cursor.close()
    return result

def StateDailyPres(state, president):
    query = """
    with temp as (select term_start as s, term_end as e from president where president_name = %0s)
    select dt, averagetemperature from temp, state
    where dt >= s and dt <= e
    and state = %1s
    order by dt asc
    """

    cursor = connection.cursor()
    cursor.execute(query, [president, state])
    result = cursor.fetchall()
    cursor.close()
    return result

def StateParty(state, dtBottom, dtTop):
    query = """
    select party, avg(averagetemperature) from president, state
    where dt < term_end and dt > term_start
    and dt >= to_date(%0s, \'YYYY-MM-DD\') and dt <= to_date(%1s, \'YYYY-MM-DD\')
    and state = %2s
    group by party
    """

    cursor = connection.cursor()
    cursor.execute(query, [dtBottom, dtTop, state])
    result = cursor.fetchall()
    cursor.close()
    return result

def StateAvgPres(state):
    query = """
    with temp as (select president_name, avg(averagetemperature) as avg from state, president
    where dt < term_end and dt > term_start
    and state = %0s
    group by president_name)
    select president.president_name, temp.avg from temp, president
    where temp.president_name = president.president_name
    order by term_start asc
    """

    cursor = connection.cursor()
    cursor.execute(query, [state])
    result = cursor.fetchall()
    cursor.close()
    return result

#Country
def CountryYearlyAvg(country, yrBottom, yrTop):
    query = """
    with temp as (select country, extract(year from dt) as yr, avg(averagetemperature) as yearlyavg from country
    group by extract(year from dt), country.country)
    select yr as year, president_name as president, yearlyavg from temp, president
    where yr <= extract(year from term_end) and yr >= extract(year from term_start) 
    and yr <= %0s and yr >= %1s
    and country = %2s
    order by year
    """

    cursor = connection.cursor()
    cursor.execute(query, [yrTop, yrBottom, country])
    result = cursor.fetchall()
    cursor.close()
    return result

def CountryMaxPres(country):
    query = """
    with temp as(
    select president_name as pres, max(averagetemperature) as mx from country, president
    where dt <= term_end and dt >= term_start
    and country = %0s
    group by president_name)
    select pres, mx from temp, president
    where temp.pres = president.president_name
    order by term_start
    """

    cursor = connection.cursor()
    cursor.execute(query, [country])
    result = cursor.fetchall()
    cursor.close()
    return result

def CountryParty(country, dtBottom, dtTop):
    query = """
    select party, avg(averagetemperature) from president, country
    where dt < term_end and dt > term_start
    and dt >= to_date(%0s, \'YYYY-MM-DD\') and dt <= to_date(%1s, \'YYYY-MM-DD\')
    and country = %2s
    group by party
    """

    cursor = connection.cursor()
    cursor.execute(query, [dtBottom, dtTop, country])
    result = cursor.fetchall()
    cursor.close()
    return result

def CountryAvgPres(country):
    query = """
    with temp as (select president_name, avg(averagetemperature) as avg from country, president
    where dt < term_end and dt > term_start
    and country = %0s
    group by president_name)
    select president.president_name, temp.avg from temp, president
    where temp.president_name = president.president_name
    order by term_start asc
    """

    cursor = connection.cursor()
    cursor.execute(query, [country])
    result = cursor.fetchall()
    cursor.close()
    return result