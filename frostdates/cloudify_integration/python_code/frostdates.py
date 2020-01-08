# ! pip install netCDF4

# Import
import netCDF4 # python API to work with netcdf (.nc) files
import os
import datetime
from osgeo import gdal, ogr, osr
import numpy as np # library to work with matrixes and computations in general
#import matplotlib.pyplot as plt # plotting library
from auxiliary_classes import convert_time,convert_time_reverse,kelvin_to_celsius,kelvin_to_celsius_vector,Grid,Image,subImage
import json
import geojson, gdal, subprocess

from frostdates_params import DAY_IN_ROW, START_HOUR_DAY, END_HOUR_DAY, FROST_DEGREE, START_YEAR, END_YEAR, PROBABILITY, INPUT_LOGLEVEL, EXPORT_FOLDER, DATA_FOLDER, START_LON, START_LAT, END_LON, END_LAT,  setup_logger, process_id

# Auxiliary Functions
def print_geojson(tname, tvalue, fname, startdoc, position,endloop): #for printing to geojson - start,end,attributes
    fname = fname +".geojson"
    pmode="a"
    if startdoc==1:
        with open(fname, mode="w", encoding='utf-8') as f1:
            tstring = "{\n\"type\": \"FeatureCollection\",\n\"features\": ["
            print(tstring, file=f1)
            f1.close()
    else:
        if position==1:
            with open(fname, mode=pmode, encoding='utf-8') as f1:
                print("{", file=f1)
                f1.close()  
        elif position==2:
            with open(fname, mode=pmode, encoding='utf-8') as f1:
                if endloop==0:
                    print("}\n},", file=f1)
                    f1.close()
                else:
                    print("}\n}\n]\n}", file=f1)
                    f1.close()
        elif position==3:
            with open(fname, mode=pmode, encoding='utf-8') as f1:
                ttext = "\"" + str(tname) + "\": \"" +str(tvalue) + "\""
                print(ttext, file=f1) 
                f1.close()
        else:
             with open(fname, mode=pmode, encoding='utf-8') as f1:
                ttext = "\"" + str(tname) + "\": \"" +str(tvalue) + "\","
                print(ttext, file=f1) 
                f1.close() 
                
def print_geojson_2(longitude, latitude, fname): #for printing to geojson - geometry, longitude, latitude
    tstring = "\"type\": \"Feature\",\n\"geometry\": {\n\"type\": \"Point\",\n\"coordinates\": [" + str(longitude) + ","+ str(latitude) + "]\n},\n\"properties\": {"
    fname = fname +".geojson"
    with open(fname, mode="a", encoding='utf-8') as f1:
            print(tstring, file=f1)
            f1.close()
            
def probabilitydate(inputlist, probability, first):#calculate frost date with selected probability from list of frost dates of each year
    listlong = len(inputlist)
    if listlong == 1:
        outputdate = 0
        return outputdate
    elif listlong == 0:
        outputdate = 0
        return outputdate
    else:
        orderlist = orderedlist(inputlist)
        valuelist = daynumberlist(orderlist)
        value = 0
        if first==1:
            value = int(gauss_value(valuelist, probability))
        else: 
            probability=100-probability
            value = int(gauss_value(valuelist, probability))
        outputdate = orderlist[0] + timedelta(days=value)
        return outputdate
    
def same_year(daylong): #change date to same year (2030) for next calculation
        sdaylong = str(daylong)
        tday = int(sdaylong[8:10])
        tmonth = int(sdaylong[5:7])
        sameyear = date(2030, tmonth, tday)
        return sameyear
    
def gauss_value(inputlist, probability): #value of gaussian probability from values of input list
    mean = np.mean(inputlist)
    sigma = np.std(inputlist)
    values = np.random.normal(mean,sigma,10000)
    value = np.percentile(values,probability)
    return value

def orderedlist(inputlist): #sort list by date
    listlong = len(inputlist)
    for j in range (0,listlong-1,1):
        for i in range(j+1, listlong, 1):
            firstday = inputlist[j]
            secondday = inputlist[i]
            sfirstday = str(firstday)
            ssecondday = str(secondday)
            fday = int(sfirstday[8:10])
            fmonth = int(sfirstday[5:7])
            sday = int(ssecondday[8:10])
            smonth = int(ssecondday[5:7])
            if fday<10:
                firstval=str(fmonth)+"0"+str(fday)
            else:
                firstval=str(fmonth)+str(fday)
            if sday<10:
                secondval=str(smonth)+"0"+str(sday)
            else:
                secondval=str(smonth)+str(sday)
            firstvalue = int(firstval)
            secondvalue = int(secondval)
            if secondvalue < firstvalue:
                inputlist[j]=secondday
                inputlist[i]=firstday
    return inputlist

def daynumberlist(orderlist): #from ordered dates to number of days from first date 
    listlong = len(orderlist)
    outputlist=[]
    outputlist.append(0)
    for i in range(1, listlong, 1):
        difference = orderlist[i] - orderlist[0]
        outputlist.append(difference.days)
    return outputlist    
    
#  Find frost dates: function for one place
from datetime import date, timedelta
def findfrostdates(latitude,longitude,year,frostdegree,dayinrow,starthourday,endhourday,fnamefrostdates,im,firstlist, lastlist,nmbfrdayslist):
    numbfrostdays=0 # for calculating numb of frost days
        
    #determination of winter and summer:
    wintermonth=1
    summermonth=7
    if latitude<0:
        wintermonth=7
        summermonth=1
    
    # Last spring frost date:
    startmonth=wintermonth
    endmonth=summermonth
    lastfrostday=0
    daysbefore=0
    startdate=1
    enddate=1
    if endmonth == 1:
        endmonth=12
        enddate=31
    sdate = date(year, startmonth, startdate)   # start date for searching last frost date
    edate = date(year, endmonth, enddate)   # end date for searching last frost date
    delta = edate - sdate       # as timedelta
    for i in range(delta.days):
        daylong = sdate + timedelta(days=i)
        sdaylong = str(daylong)
        tday = int(sdaylong[8:10])
        tmonth = int(sdaylong[5:7])
        tyear = int(sdaylong[0:4])
        daymin = 50 # start value
        for hour in range(starthourday, endhourday+1, 1): # for specific hours (all day,only sunrise hours,..)
            time=convert_time_reverse(datetime.datetime(tyear, tmonth, tday, hour, 0))
            slice_dictionary={'lon':[longitude,],'lat':[latitude],'time':[int(time)]}
            currenttemp=kelvin_to_celsius_vector(im.slice('t2m_NON_CDM',slice_dictionary))
            if currenttemp < daymin:
                daymin = currenttemp
        if daymin <= frostdegree:  # frostday?
            numbfrostdays+=1
            lastfrostday=daylong
            if daysbefore>=dayinrow-1:
                lastfrostday=daylong
            daysbefore=+1
        else:
            daysbefore=0
    
    tvarname = "LastD"+ str(year)
    print_geojson(tvarname, lastfrostday, fnamefrostdates, 0, 0, 0)
    if lastfrostday!= 0:
        tvalue = same_year(lastfrostday)
        lastlist.append(tvalue)
                
    # First autumn frost date:
    startmonth=summermonth
    endmonth=wintermonth
    firstfrostday=0
    daysbefore=0
    cutfrost=0
    enddate=1
    startdate=1
    if endmonth == 1:
        endmonth=12
        enddate=31
        
    sdate = date(year, startmonth, startdate)   # start date of searching
    edate = date(year, endmonth, enddate)   # end date of searching
    delta = edate - sdate       # as timedelta
    for i in range(delta.days):
        daylong = sdate + timedelta(days=i)
        sdaylong = str(daylong)
        tday = int(sdaylong[8:10])
        tmonth = int(sdaylong[5:7])
        tyear = int(sdaylong[0:4])
        daymin = 50 # start value
        for hour in range(starthourday, endhourday+1, 1): # for specific hours (all day,only sunrise hours,..)
            time=convert_time_reverse(datetime.datetime(tyear, tmonth, tday, hour, 0))
            slice_dictionary={'lon':[longitude],'lat':[latitude],'time':[int(time)]}
            currenttemp=kelvin_to_celsius_vector(im.slice('t2m_NON_CDM',slice_dictionary))
            if currenttemp < daymin:
                daymin = currenttemp
        if daymin <= frostdegree:  # frostday?
            numbfrostdays+=1
            if daysbefore>=(dayinrow-1) and cutfrost==0:
                firstfrostday=daylong
                cutfrost=1
            daysbefore=+1
        else:
            daysbefore=0
       
    tvarname = "FirstD"+str(year)
    print_geojson(tvarname, firstfrostday, fnamefrostdates, 0, 0, 0)
    if firstfrostday!= 0:
        tvalue = same_year(firstfrostday)
        firstlist.append(tvalue)
    # Frostfreeperiod
    frostfreeperiod=0
    if firstfrostday!=0 and lastfrostday!=0:
        if latitude>0:
            frostfreeperiod =  firstfrostday-lastfrostday
            frostfreeperiod = frostfreeperiod.days
        else:
            firstyeardate = date(year, 1, 1)   # start date of year
            lastyeardate = date(year, 12, 31)   # end date of year
            frostfreeperiod =  (firstfrostday-firstyeardate)+(lastyeardate-lastfrostday)
    tvarname = "Period"+ str(year)
    print_geojson(tvarname, frostfreeperiod, fnamefrostdates, 0, 0, 0)
    
    tvarname = "FrDays"+ str(year) 
    print_geojson(tvarname, numbfrostdays, fnamefrostdates, 0, 0, 0)
    nmbfrdayslist.append(numbfrostdays)
    
# Find frost dates: function for selected years
def frostdatesyearly(latorder,lonorder,startyear,endyear,frostdegree,dayinrow,starthourday,endhourday,fnamefrostdates,endloop,datafolder,probability):
    print_geojson("", "", fnamefrostdates, 0, 1,0)
    firstlist = []
    lastlist = []
    nmbfrdayslist = []
    
    for year in range(startyear, endyear+1, 1):
        source = datafolder + '/' + str(year) + '.nc' 
        im=Image(netCDF4.Dataset(source,'r'))   
        longlist = im.get_data().variables['lon'][:]
        latlist= im.get_data().variables['lat'][:]
        longitude = longlist [lonorder]   
        latitude = latlist[latorder]
        if year == startyear:
            print_geojson_2(longitude, latitude, fnamefrostdates)
        findfrostdates(latitude,longitude,year,frostdegree,dayinrow,starthourday,endhourday,fnamefrostdates,im,firstlist,lastlist,nmbfrdayslist)

    firstprobday = probabilitydate(firstlist, probability, 1)
    lastprobday = probabilitydate(lastlist, probability, 0)
    namefirstprob = "FirstD" + str(probability) 
    namelastprob = "LastD" + str(probability) 
    print_geojson(namelastprob, lastprobday, fnamefrostdates, 0, 0, 0)
    print_geojson(namefirstprob, firstprobday, fnamefrostdates, 0, 0, 0)
    
    nameperiodprob = "Period" + str(probability) 
    frostfreeperiod=0
    if firstprobday!=0 and lastprobday!=0:
        if latitude>0:
            frostfreeperiod =  firstprobday-lastprobday
            frostfreeperiod = frostfreeperiod.days
        else:
            firstyeardate = date(2030, 1, 1)   # start date of year
            lastyeardate = date(2030, 12, 31)   # end date of year
            frostfreeperiod =  (firstprobday-firstyeardate)+(lastyeardate-lastprobday) 
    
    print_geojson(nameperiodprob, frostfreeperiod, fnamefrostdates, 0, 0, 0)
    tmeannmb = np.mean(nmbfrdayslist)
    meannmb = int(np.round(tmeannmb, decimals=0, out=None))
    print_geojson("AvgFrDays", meannmb, fnamefrostdates, 0, 3, 0)
    print_geojson("", "", fnamefrostdates, 0, 2,endloop)
    
# Find frost dates: function for selected latitudes, longitudes
def frostdatesplaces(startlat, startlon, endlat, endlon, startyear,endyear,frostdegree,dayinrow,starthourday,endhourday,exportfolder,datafolder,fnamefrostdates1,probability):
        setup_logger('debug', os.path.join(OUTPUT_FOLDER,'debug.log'))
        logger = logging.getLogger('debug')
        logger.info("Starting frostdates algorithm...")
    
        fnamefrostdates = exportfolder + "/" +fnamefrostdates1
        print_geojson("", "", fnamefrostdates, 1, 0,0)
        endloop=0
        for latorder in range(startlat, endlat+1, 1):
            for lonorder in range(startlon, endlon+1, 1):
                if latorder==endlat and lonorder==endlon:
                    endloop=1
                frostdatesyearly(latorder,lonorder,startyear,endyear,frostdegree,dayinrow,starthourday,endhourday,fnamefrostdates,endloop,datafolder,probability)
        logger.info("Scenario succeeded!")
                
if __name__ == "__main__":
  try:
    frostdatesplaces(startlat, startlon, endlat, endlon, startyear,endyear,frostdegree,dayinrow,starthourday,endhourday,exportfolder,datafolder,fnamefrostdates,probability)
  except Exception as err:
    setup_logger('error_logger', os.path.join(OUTPUT_FOLDER,'error_traceback.log'))
    error_logger = logging.getLogger('error_logger')
    error_logger.error("Process failed! Error raised: {}".format(traceback.format_exc()))
    logger = logging.getLogger('debug')
    logger.error("Process failed! Error raised: {}".format(err))