% Implementation of Double Gaussian segmentation method
% input parameters: data_gray=list of gray scale values from image
%   fo= fitting options to define extent of fit of double gaussian
%   for example:
%         fo = fitoptions('Method','NonlinearLeastSquares',...
%              'Lower',     [0,   100 ,   0, 20000,  100],...
%              'Upper',     [0.2, 3000, 0.1, 32000, 6000],...
%              'StartPoint',[0.1,  500, 0.01, 26000, 2000]);
% output: threshold used to segment data into binary field
function thr = get_double_gaussian(data_gray, fo)

    % remove noise values at high gray levels (dense minerals)
    J = data_gray<prctile(data_gray, 99);
    data_gray = data_gray(J);

    dbin       = 150;
    min_gray  = min(data_gray);
    max_gray  = max(data_gray);
    bins_gray = min_gray:dbin:max_gray;
    hist_gray = hist(data_gray,bins_gray)/length(data_gray);

    [val, i_m] = max(hist_gray);
    val_fit = bins_gray(i_m);
    
    ft = fittype(['log10(a*exp(-((x-' num2str(val_fit) ')/b)^2) + c*exp(-((x-d)/e)^2))'],'options',fo);
    [curve,gof] = fit(bins_gray',log10(hist_gray'),ft);
    
    % a, c = pre-factor  b, e=std, d= peak of smaller histogram
    fit_gray     = log10(curve.a*exp(-((bins_gray-val_fit)/curve.b).^2) + curve.c*exp(-((bins_gray-curve.d)/curve.e).^2));

    % get 2nd derivative to find the inflection of the fit
    delfit = fit_gray(2:end)-fit_gray(1:end-1);
    delfit = delfit(2:end)-delfit(1:end-1);
    
    % get minimum of delfit
    [val, i_0] = min(abs(delfit));
    grays = bins_gray(3:end);
    thr = grays(i_0);
    bthr = delfit(i_0);

    figure(1)
    hold on
    yyaxis left
    plot(bins_gray, log10(hist_gray),'k', 'linewidth', 2)
    plot(bins_gray, fit_gray,'b:','LineWidth',2)  
    set(gca, 'YColor', 'b')
    
    ylabel('log_{10}(pdf)')
    yyaxis right
    plot(bins_gray(3:end), delfit,'r-','LineWidth',2)
    plot(thr, bthr, 'r*', 'linewidth', 2)
    
    set(gca, 'YColor', 'r')
    
    xlim([bins_gray(1) bins_gray(end)])
    xlabel('gray value')
    ylabel('2nd deriv. log_{10}(pdf)')
    
    set(gca, 'fontsize', 20)
    set(gca, 'linewidth', 2)
    box on

    
    
end

