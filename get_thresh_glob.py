#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:42:30 2020

@author: mcbeck
"""

import numpy as np
from skimage import io
import skimage.filters as filters

nois = ['blur', 'pt']
#nois = ['pt']
#sizestr = 'sm'
#sizestr = 'sm_doscl_raw'
sizestr = 'big' 

fold = '/Users/mcbeck/Dropbox/HADES/segmentation/processing/data/cropfigs/'

zs = [0, 9,18,28,37,46,55,64,74,83,92,101,111,120,129,138,147,157,166,175,184,193,203,212,221,230,240,249,258,267,276,286,295,304,313,322,332,341,350,359,368,378,387,396,405,415,424,433,442,451,461,470,479,488,497,507,516,525,534,544,553,562,571,580,590,599,608,617,626,636,645,654,663,672,682,691,700,709,719,728,737,746,755,765,774,783,792,801,811,820,829,838,848,857,866,875,884,894,903,912,921,930,940,949,958,967,976,986,995,1004,1013,1023,1032,1041,1050,1059,1069,1078,1087,1096,1105,1115,1124,1133,1142,1151,1161,1170,1179,1188,1198,1207,1216,1225,1234,1244,1253,1262,1271,1280,1290,1299,1308,1317,1327,1336,1345,1354,1363,1373,1382,1391,1400,1409,1419,1428,1437,1446,1455,1465,1474,1483,1492,1502,1511,1520,1529,1538,1548,1557,1566,1575,1584,1594,1603,1612,1621,1631,1640,1649,1658,1667,1677,1686,1695,1704,1713,1723,1732,1741,1750,1759,1769,1778,1787,1796,1806,1815,1824,1833,1842,1852,1861,1870,1879,1888,1898,1907,1916,1925,1935,1944,1953,1962,1971,1981,1990,1999]
#zs = [516, 1253, 1474]    
#zs = [1253]

for noistr in nois:
    txtf = 'output/thr_glob_z'+str(zs[0])+'_'+str(zs[-1])+'_'+sizestr+'_'+noistr+'.txt'    
    totlines = "noise iso li mean otsu triangle yen \n"
    ni=0
    while ni<=6:
        nstr = noistr+str(ni)
        totvals = []
        if len(zs)==1:
            zstr = str(zs[0])
            while len(zstr)<4:
                zstr = '0'+zstr
                        
            nfil = 'wg04'+sizestr+'_'+zstr+'_'+nstr+'.tif'
            print(nfil)
            
            image = io.imread(fold+nfil)
            totvals = image
        else:
            for z in zs:   
                zstr = str(z)
                while len(zstr)<4:
                    zstr = '0'+zstr
                            
                nfil = 'wg04'+sizestr+'_'+zstr+'_'+nstr+'.tif'
                print(nfil)
                
                image = io.imread(fold+nfil)
                vals = image.flatten()
                totvals.append(vals)
        
            totvals = np.array(totvals)
            
        #thrvals = [filters.threshold_isodata(totvals), filters.threshold_otsu(totvals), filters.threshold_yen(totvals)]
        
        thrvals = [filters.threshold_isodata(totvals), filters.threshold_li(totvals), filters.threshold_mean(totvals), filters.threshold_otsu(totvals), filters.threshold_triangle(totvals), filters.threshold_yen(totvals)]               
                               
        frmt = "%d %f %f %f %f %f %f \n" % (ni, thrvals[0], thrvals[1], thrvals[2],thrvals[3],thrvals[4],thrvals[5])
        #print('image:', thrimage)
        totlines = totlines+frmt
        print(totlines)
        
        
        ni=ni+1
    
    f = open(txtf, "w")
    f.write(totlines)
    f.close()
    
    print(txtf) 