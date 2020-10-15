###########################################################################
### Estimation of Slope along the boundary using the buffer distance    ###
### Author : Lakshmi E                                                  ###
### Last Edit: 13-April-2020                                            ###
###########################################################################

import arcpy
import os,glob
import numpy as np
from arcpy.sa import *
from arcpy import env
import dbf
import csv

# work in the current directory
env.workspace=(input("give the current directory:"))                            #'C:\Users\Laks\Desktop\REGSim module'
dirpath = os.getcwd()

#assign the buffer distance 
buffer_dist = input('Buffer distance between the study area (meters):')
num_pts     = input('no. of points considered across the boundary:')

# Load required toolboxes
arcpy.ImportToolbox(".\Module\CreatePointsLines.tbx")
arcpy.CheckOutExtension("spatial")

# create buffer in and out
def buffer(bound):
    print('Creating buffer inside and outside the boundary area...')
    arcpy.Buffer_analysis(bound, 'buffin{0}.shp'.format(buffer_dist),'-{0}'.format(buffer_dist),'FULL','ROUND','NONE','')
    arcpy.Buffer_analysis(bound, 'bufout{0}.shp'.format(buffer_dist),'{0}'.format(buffer_dist),'FULL','ROUND','NONE','')

bound='bound_hmda.shp'                          

buffer(bound)

# create points to the feature class
print('Converting polygon to line feature class...')

def ext_pts(bound,boundin,boundout,bufin,bufout):
    list=[bound,boundin,boundout,bufin,bufout]                        
    for i in list:
        print(i)
        arcpy.FeatureToLine_management(i,'{0}_line.shp'.format(i[:-4]),'','ATTRIBUTES')
        arcpy.AddField_management('{0}_line.shp'.format(i[:-4]),'Length','FLOAT','','','','','NULLABLE','NON_REQUIRED',"")
        arcpy.CalculateField_management('{0}_line.shp'.format(i[:-4]), "Length", "!SHAPE.Length!", "PYTHON", "")
        length = arcpy.da.SearchCursor('{0}_line.shp'.format(i[:-4]), "Length").next()[0]
        dist_intv = length/num_pts #point_num
        arcpy.CreatePointsLines_CreatePointsLines('{0}_line.shp'.format(i[:-4]),'INTERVAL BY DISTANCE', 'BEGINNING','NO','',dist_intv,'NO','{0}_pts.shp'.format(i[:-4]))

print('Created points to the feature class...')
bound = 'bound_hmda.shp'
boundin = 'bndin_hmda.shp'
boundout = 'bndou_hmda.shp'
bufin = 'buffin{0}.shp'.format(buffer_dist)
bufout = 'bufout{0}.shp'.format(buffer_dist)

ext_pts(bound,boundin,boundout,bufin,bufout)
              
# extract elevation value to the points
print('Extracting the elevation data from the raster to the point featureclass...')

def pts_value(raster,list):    
    for i in raster:
        print(i)
        ExtractValuesToPoints('bound_hmda_pts.shp','{0}'.format(i),'bound{1}_{0}_extrpts{2}_{3}.shp'.format(i[9:12],buffer_dist,num_pts,i[2:4]),'INTERPOLATE','VALUE_ONLY')
        arcpy.AddField_management('bound{1}_{0}_extrpts{2}_{3}.shp'.format(i[9:12],buffer_dist,num_pts,i[2:4]),"Slope","DOUBLE","", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        for j,z in zip(list,list_bound):
            print(j)
            print(z)
            ExtractValuesToPoints('{0}_pts.shp'.format(j[:-4]),'{0}'.format(i),'{0}_{1}_extrpts.shp'.format(j[0:5],i[9:12]),'INTERPOLATE','VALUE_ONLY')
            ExtractValuesToPoints('{0}_pts.shp'.format(z[:-4]),'{0}'.format(i),'{0}_{1}_extrpts.shp'.format(z[0:5],i[9:12]),'INTERPOLATE','VALUE_ONLY')
        for k,l in zip(list_bound,list):
            arcpy.Near_analysis('{0}_{1}_extrpts.shp'.format(k[0:5],i[9:12]),'{0}_{1}_extrpts.shp'.format(l[0:5],i[9:12]),'','NO_LOCATION','NO_ANGLE')
            arcpy.JoinField_management('{0}_{1}_extrpts.shp'.format(k[0:5],i[9:12]),'NEAR_FID','{0}_{1}_extrpts.shp'.format(l[0:5],i[9:12]),"FID","#")
            arcpy.AddField_management('{0}_{1}_extrpts.shp'.format(k[0:5],i[9:12]), "Slope", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            arcpy.AddField_management('{0}_{1}_extrpts.shp'.format(l[0:5],i[9:12]), "Slope", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management('bndou_{0}_extrpts.shp'.format(i[9:12]), "Slope", "(!RASTERVALU!- !RASTERVA_1!) / !NEAR_DIST!", "PYTHON_9.3", "")
        arcpy.CalculateField_management('bndin_{0}_extrpts.shp'.format(i[9:12]), "Slope", "(!RASTERVA_1!-!RASTERVALU!) / !NEAR_DIST!", "PYTHON_9.3", "")
           
 
raster=sorted(glob.glob("*_GWL_*.tif"))
list=['buffin{0}.shp'.format(buffer_dist),'bufout{0}.shp'.format(buffer_dist)]
list_bound = ['bndin_hmda.shp','bndou_hmda.shp']

pts_value(raster,list)    

# estimae the average slope
print('Estimating slope in each point of the boundary area...')   
filesav = []
def avg_sl(raster):  
    for i in raster:
        list=sorted(glob.glob('bnd*{0}_extrpts.dbf'.format(i[9:12])))
        print(list)
        tabin=dbf.Table('{0}'.format(list[0]))
        tabin.open()
        tabout=dbf.Table('{0}'.format(list[1]))
        tabout.open()
        tabbou=dbf.Table('bound{1}_{0}_extrpts{2}_{3}.dbf'.format(i[9:12],buffer_dist,num_pts,i[2:4]))
        tabbou.open(mode=dbf.READ_WRITE)
    
        for l,j,k in zip(tabin,tabout,range(0,len(tabbou))):
            mas=l[-1]
            sla=j[-1]
            res=((mas+sla)/2)        
            with tabbou[k] as record:
                record.slope=res

        tabin.close()
        tabout.close()
        tabbou.close()
        print(tabbou)
        
        f = 'bound{1}_{0}_extrpts{2}_{3}'.format(i[9:12],buffer_dist,num_pts,i[2:4])
        filesav.append(f)
                
raster=sorted(glob.glob("*_GWL_*.tif"))

avg_sl(raster)

print(' Saving the output file')
with open('output.csv', 'wb') as output:
    csvwriter = csv.writer(output,dialect='excel')
    for row in filesav:
        csvwriter.writerow([row])
    output.close()

#end of the script




