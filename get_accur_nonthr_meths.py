# -*- coding: utf-8 -*-
"""
Script to segment fractures with thresholds
"""
#from skimage import data
import numpy as np
import statistics as stat
from skimage import io
import skimage.filters as filters


# decide if only using the best methods (best)
# decide if using a constant threshold based on least noisy image
#zsamptxt = 'zall_'
zsamptxt = '' 

# resolutions
#sizs = ['sm_doscl_raw']
#sizs = ['big']
sizs = ['sm']
crstr = '_crop'
# different methods of adding noise
nois = ['pt', 'blur']
#nois = ['pt']

# number of noise iterations
numnois= 6

fold = '/Users/mcbeck/Dropbox/HADES/segmentation/processing/data/cropfigs/'

for noistr in nois:

    for sizestr in sizs:
    
        zbigs = [516, 544, 617, 1253, 1474]
        if 'all' in zsamptxt:
            zbigs = [0, 9,18,28,37,46,55,64,74,83,92,101,111,120,129,138,147,157,166,175,184,193,203,212,221,230,240,249,258,267,276,286,295,304,313,322,332,341,350,359,368,378,387,396,405,415,424,433,442,451,461,470,479,488,497,507,516,525,534,544,553,562,571,580,590,599,608,617,626,636,645,654,663,672,682,691,700,709,719,728,737,746,755,765,774,783,792,801,811,820,829,838,848,857,866,875,884,894,903,912,921,930,940,949,958,967,976,986,995,1004,1013,1023,1032,1041,1050,1059,1069,1078,1087,1096,1105,1115,1124,1133,1142,1151,1161,1170,1179,1188,1198,1207,1216,1225,1234,1244,1253,1262,1271,1280,1290,1299,1308,1317,1327,1336,1345,1354,1363,1373,1382,1391,1400,1409,1419,1428,1437,1446,1455,1465,1474,1483,1492,1502,1511,1520,1529,1538,1548,1557,1566,1575,1584,1594,1603,1612,1621,1631,1640,1649,1658,1667,1677,1686,1695,1704,1713,1723,1732,1741,1750,1759,1769,1778,1787,1796,1806,1815,1824,1833,1842,1852,1861,1870,1879,1888,1898,1907,1916,1925,1935,1944,1953,1962,1971,1981,1990,1999]
        
        txtf = 'output/comp_segment_mask_'+zsamptxt+noistr+'_'+sizestr+crstr+'_hor2D.txt'
        totlines = "z noise method frac_vol corr_tot num_tot accur poro \n"
        for imn in zbigs:
            imstr = str(imn)
            while len(imstr)<4:
                imstr = '0'+imstr
            
            # get the original image
            nstr = noistr+'0'
            
            figr = sizestr+'_z'+imstr+'_'+nstr
            nfil = 'wg04'+sizestr+'_'+imstr+crstr+'_'+nstr+'.tif'
            print(nfil)
            
            imtrue = io.imread(fold+nfil)
            vals = imtrue.flatten()
            vals = [float(v) for v in vals]
            tmu = stat.mean(vals)
            
            fractrue = imtrue>tmu
            solidtrue = imtrue<tmu  
            
            fracvol_obs = sum(fractrue.flatten())
            solvol_obs = sum(solidtrue.flatten())
  
            ni=0
            while ni<=numnois:
                nstr = noistr+str(ni)
        
                figr = sizestr+'_z'+imstr+'_'+nstr
                nfil = 'wg04'+sizestr+'_'+imstr+crstr+'_'+nstr+'.tif'
                print(nfil)
                
                image = io.imread(fold+nfil)
                masks = [filters.threshold_local(image, 17, 'gaussian'), filters.threshold_local(image, 17, 'mean'), filters.threshold_local(image, 17, 'median'), filters.threshold_local(image, 21, 'mean'), filters.threshold_local(image, 25, 'mean'), filters.threshold_local(image, 31, 'mean'), filters.threshold_niblack(image), filters.threshold_sauvola(image)]               

                #x=abc
                mi=1
                for mask in masks:
                
                    frac = image>mask

                    correct = frac==fractrue
                    correct = correct.flatten()
                    numcor = np.sum(correct)
                    totvox = len(correct)
 
                    isfracg = frac==True
                    isfrac = isfracg.flatten()
                    fracvol = np.sum(isfrac)
                    poro = fracvol/totvox
                    
                    # z noise method frac_vol corr_tot num_tot accur poro
                    frmt= "%s %d %d %d %d %d %f %f \n" % (imstr, ni, mi, fracvol, numcor, totvox, numcor/totvox, poro)
        
                    totlines= totlines+frmt
                    
        #            fig, ax = plt.subplots()
        #            ax.imshow(frac)
        #            plt.title(nstr+' '+tits[mi-1]+' m='+str(mi))
        #            plt.xticks([])
        #            plt.yticks([])
        #            plt.show()
                    print(totlines)
                    #x=abc
                    
                    mi=mi+1
        
                ni=ni+1
           
        
        print(totlines) 
        
        f = open(txtf, "w")
        f.write(totlines)
        f.close()
        
        print(txtf)  
     
