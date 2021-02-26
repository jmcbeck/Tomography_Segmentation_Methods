#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 13:20:56 2020

@author: mcbeck
"""
#from skimage import data
import numpy as np
import statistics as stat
from statistics import mode
from skimage import io
from itertools import chain

from scipy import ndimage as ndi
import matplotlib.image as mpimg

from skimage.measure import label
from skimage.filters import hessian

from skimage.segmentation import watershed
from skimage.feature import peak_local_max 
    

def get_watershed(img):
    #img = mpimg.imread(imgname)

    # calculates the euclidean distance of a pixel from the background image
    # The euclidean distance transform gives values of the euclidean distance:
    #               n
    # y_i = sqrt(sum (x[i]-b[i])**2)
    #               i
    # where b[i] is the background point (value 0) with the smallest Euclidean distance to input points x[i], and n is the number of dimensions. You can read more about this function here: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.morphology.distance_transform_edt.html
    distance = ndi.distance_transform_edt(img)
    
    # find the local peaks for each fracture in the image
    local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=img)
    # creates labels similar to the the label function in the hessian code.
    # Here I only take the labels (the first item in the returned tuple).
    # The second item is the number of features found. You can read more about this here: https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.label.html
    markers = ndi.label(local_maxi)[0]
    
    # applies the watershed algorithm to labeled image. You can read more about this here: https://scikit-image.org/docs/dev/api/skimage.segmentation.html#skimage.segmentation.watershed
    labels = watershed(-distance, markers, mask=img)
    
    # =1 for fracture
    #print(min(labels), max(labels))
    frac = labels
    frac[frac==1] = 0
    frac[frac>1] = 1

    return frac

def get_hessian(img):
    #img = mpimg.imread(imgname)
    
    
    # calculate the hessian filter
    # documentation  can be found here: https://scikit-image.org/docs/dev/api/skimage.filters.html#skimage.filters.hessian
    # the sigmas represent the scale of the filter that is
    # they are the standard deviation of the assumed gaussian kernel
    # that is used to differentiate the fractures from the 
    # homogeneous rock. Essentially what these end up being is the 
    # thickness of the border that is eventually deleted later.
    # to learn more about hessian filters read this link: https://link.springer.com/chapter/10.1007%2F978-3-319-16811-1_40
    bins = hessian(img, sigmas=[2,2])
    
    # label is an automated function that labels all of the spaces found
    # in the image. This works for basically any image filter that returns
    # a matrix of zeros and ones afaik. It replaces the ones with the label
    # number of the unique fracture that is found.
    lab = label(bins)
    
    # this line removes the borders and replaces them with the same label
    # as the homogenous rock (0).
    lab[lab == 0] = 0
    lab[lab == 1] = 0
    
    # label everything else as a fracture
    frac[frac>0] = 1
    return frac

nois = ['pt', 'blur']
#sizs = ['sm_doscl_raw']
#sizs = ['big']
sizs = ['sm'] 
crstr = '_crop'

#zs = [0, 9,18,28,37,46,55,64,74,83,92,101,111,120,129,138,147,157,166,175,184,193,203,212,221,230,240,249,258,267,276,286,295,304,313,322,332,341,350,359,368,378,387,396,405,415,424,433,442,451,461,470,479,488,497,507,516,525,534,544,553,562,571,580,590,599,608,617,626,636,645,654,663,672,682,691,700,709,719,728,737,746,755,765,774,783,792,801,811,820,829,838,848,857,866,875,884,894,903,912,921,930,940,949,958,967,976,986,995,1004,1013,1023,1032,1041,1050,1059,1069,1078,1087,1096,1105,1115,1124,1133,1142,1151,1161,1170,1179,1188,1198,1207,1216,1225,1234,1244,1253,1262,1271,1280,1290,1299,1308,1317,1327,1336,1345,1354,1363,1373,1382,1391,1400,1409,1419,1428,1437,1446,1455,1465,1474,1483,1492,1502,1511,1520,1529,1538,1548,1557,1566,1575,1584,1594,1603,1612,1621,1631,1640,1649,1658,1667,1677,1686,1695,1704,1713,1723,1732,1741,1750,1759,1769,1778,1787,1796,1806,1815,1824,1833,1842,1852,1861,1870,1879,1888,1898,1907,1916,1925,1935,1944,1953,1962,1971,1981,1990,1999]

zs = [516, 544, 617, 1253, 1474]
#zs = list(range(2000))
numnois= 6
mci = 10

fold = '/Users/mcbeck/Dropbox/HADES/segmentation/processing/data/cropfigs/'
 

for noistr in nois:
    for sizestr in sizs:
        txtf = 'output/comp_segment_water_hess_'+noistr+'_'+sizestr+crstr+'_hor2D.txt'
        totlines = "z noise method frac_vol corr_tot num_tot accur poro \n"
        
        for z in zs:        
            zstr = str(z)
            while len(zstr)<4:
                zstr = '0'+zstr
                
            # get the original image
            nstr = noistr+'0'
            
            nfil = 'wg04'+sizestr+'_'+zstr+crstr+'_'+nstr+'.tif'
            print(nfil)
            
            imtrue = io.imread(fold+nfil)
            vals = imtrue.flatten()
            vals = [float(v) for v in vals]
            tsig = stat.stdev(vals)
            tmu = stat.mean(vals)
            
            fractrue = imtrue>tmu
            solidtrue = imtrue<tmu  
            
            #isfractrue = fractrue==True
            #issoltrue = fractrue==False
            
            ni=0
            while ni<=numnois:
                nstr = noistr+str(ni)
        
                nfil = 'wg04'+sizestr+'_'+zstr+crstr+'_'+nstr+'.tif'
                print(nfil)                
                #image = io.imread(fold+nfil)
                
                #fil = 'wg04'+sizestr+'_'+zstr+'.tif'
                img = mpimg.imread(fold+nfil)
            
                #fracs= [get_watershed(img), get_hessian(img)]
                
                
                mi=mci
                while mi<=mci+1:
                    if mi==mci:
                        frac = get_watershed(img)
                    else:
                        frac = get_hessian(img)
                        
                    #frac = frac>1
                    #print(frac)
                        
                    correct = frac==fractrue
                    correct = correct.flatten()
                    numcor = np.sum(correct)
                    totvox = len(correct)
     
                    isfracg = frac==True
                    isfrac = isfracg.flatten()
                    fracvol = np.sum(isfrac)
                    poro = fracvol/totvox
                    
                    # z noise method frac_vol corr_tot num_tot accur poro
                    frmt= "%s %d %d %d %d %d %f %f \n" % (zstr, ni, mi, fracvol, numcor, totvox, numcor/totvox, poro)
        
                    totlines= totlines+frmt
                    print(totlines)
                    mi=mi+1
                
                # also save the localization of the detected fractures?
                
                
                ni=ni+1
        
        print(totlines) 
        
        f = open(txtf, "w")
        f.write(totlines)
        f.close()
        
        print(txtf)  
    
    
    
    