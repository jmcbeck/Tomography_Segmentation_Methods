close all
clearvars

make_raw_crop = 1;
make_noise_crop = 1;
% make ground truth images by standard thresholding segmentation
dim = '';
%siz = 'big'; % low resolution
siz = 'sm'; % high resolution
%siz = 'sm_doscl_raw';

foldn = ['data/cropfigs/wg04' siz '_' dim];
    
thrbig = 29700;
thrsm = 28800;

if regexp(siz, 'big')
    % statistics of grey levels from get_gray_stats.m
    globmu = 3.1111e+04;
    globsig = 1.0425e+03;
    thr = thrbig;
else
    thr = thrsm;
    globmu = 3.2240e+04;
    globsig = 1.8349e+03;
end

% level of noise

%zs = [0, 9,18,28,37,46,55,64,74,83,92,101,111,120,129,138,147,157,166,175,184,193,203,212,221,230,240,249,258,267,276,286,295,304,313,322,332,341,350,359,368,378,387,396,405,415,424,433,442,451,461,470,479,488,497,507,516,525,534,544,553,562,571,580,590,599,608,617,626,636,645,654,663,672,682,691,700,709,719,728,737,746,755,765,774,783,792,801,811,820,829,838,848,857,866,875,884,894,903,912,921,930,940,949,958,967,976,986,995,1004,1013,1023,1032,1041,1050,1059,1069,1078,1087,1096,1105,1115,1124,1133,1142,1151,1161,1170,1179,1188,1198,1207,1216,1225,1234,1244,1253,1262,1271,1280,1290,1299,1308,1317,1327,1336,1345,1354,1363,1373,1382,1391,1400,1409,1419,1428,1437,1446,1455,1465,1474,1483,1492,1502,1511,1520,1529,1538,1548,1557,1566,1575,1584,1594,1603,1612,1621,1631,1640,1649,1658,1667,1677,1686,1695,1704,1713,1723,1732,1741,1750,1759,1769,1778,1787,1796,1806,1815,1824,1833,1842,1852,1861,1870,1879,1888,1898,1907,1916,1925,1935,1944,1953,1962,1971,1981,1990,1999];
zs = (0:1:1999);
%zs = (562:1999)

% special selected
%zs = [516, 544, 617, 1253, 1474];
%zs = [516, 1253, 1474];
%stds = [2 4 6 8 10 20].*globsig;
stds = [0.5 1 2 3 4 5].*globsig;

for zi=1:length(zs)
    z = zs(zi);
    filen = num2str(z);
    while length(filen)<4
       filen = ['0' filen]; 
    end
       
    
    slice = [foldn filen '.tif'];
    A = imread(slice);
    vals = double(reshape(A, 1, numel(A)));
    
    if make_raw_crop && regexp(siz, 'sm') && isempty(regexp(siz, 'sm_doscl', 'once'))
        Acrop = A((200:1200), (200:1200));

        fcrop = [foldn filen '_crop.tif'];
        imwrite(uint16(Acrop), fcrop, 'tif');
        disp(fcrop)
    end
    
    
    %rng = [globmu-0.05*globsig globmu+0.05*globsig];
    %binEs = linspace(globmu-globsig, globmu+globsig, 1000);
 
    log = A<thr; 
    Afrac= zeros(size(log));
    Afrac(log) = 1;
    Ascale = Afrac*globmu;
    
    %Ascale = uint16(Ascale);
    % A scale is the ground truth
    fname = [foldn filen '_pt0.tif'];
    imwrite(uint16(Ascale), fname, 'tif');
    disp(fname)
    
    if make_noise_crop && regexp(siz, 'sm') && isempty(regexp(siz, 'sm_doscl', 'once'))
        Acrop = Ascale((200:1200), (200:1200));

        fcrop = [foldn filen '_crop_pt0.tif'];
        imwrite(uint16(Acrop), fcrop, 'tif');
        disp(fcrop)
    end
    
    dims = size(Afrac); 
    for si=1:length(stds)
        st = stds(si);
        noises = normrnd(0, st, dims(1), dims(2));
        
        Anoise = Ascale+noises;

        fname = [foldn filen '_pt' num2str(si) '.tif'];
        imwrite(uint16(Anoise), fname, 'tif');
        disp(fname)
        
        
        % if making sm images, then also make cropped version
        % so that weka can read it
        if make_noise_crop && regexp(siz, 'sm') && isempty(regexp(siz, 'sm_doscl', 'once'))
            Acrop = Anoise((200:1200), (200:1200));

            fcrop = [foldn filen '_crop_pt' num2str(si) '.tif'];
            imwrite(uint16(Acrop), fcrop, 'tif');
            disp(fcrop)
        end

    end
    
end