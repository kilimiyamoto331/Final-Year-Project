function comparePolarFDs( fd1,fd2 );
% Plot the FDs on two a polar plots. One with linear magnitude scaling and
% the othe rwith log-magnitude scaling.

% Ensure FDs have the same length - pad as necessary
lengthDiff=length(fd1)-length(fd2);
if lengthDiff == 0
    nFDs=length(fd1);
else
    nFDs=max(length(fd1),length(fd2));
    temp=zeros(nFDs,1);
    if length(fd1) < nFDs
        temp(1:length(fd1))=fd1;
        shift=floor(nFDs/2)-floor(length(fd1)/2);
        fd1=circshift(temp,[shift,0]);
    else
        temp(1:length(fd2))=fd2;
        shift=floor(nFDs/2)-floor(length(fd2)/2);
        fd2=circshift(temp,[shift,0]);
    end;
end;

minIndex=-floor(nFDs/2);
maxIndex=minIndex+nFDs-1;
curveLineSpec1='b+';
startLineSpec1='rs';
curveLineSpec2='ro';
startLineSpec2='rs';

% Plot FDs in polar form
fdLimit=10;
if minIndex < -fdLimit
    pmin=-fdLimit;
else
    pmin=minIndex;
end;
if maxIndex > fdLimit
    pmax=fdLimit;
else
    pmax=maxIndex;
end;
plotRange=[pmin:pmax];
indexRange=plotRange-minIndex+1;
[fdArg1,fdMag1]=cart2pol(real(fd1(indexRange)),imag(fd1(indexRange)));
[fdArg2,fdMag2]=cart2pol(real(fd2(indexRange)),imag(fd2(indexRange)));
fdMaxMag=max(max(fdMag1),max(fdMag2));

figure;

% Linear scale
subplot(1,2,1);
polar(fdArg1,fdMag1,'bo');
hold on;
polar(fdArg2,fdMag2,'ro');
text=sprintf('FDs for %d\\leqn\\leq%d (Linear Magnitudes)',pmin,pmax);
title(text);

% Error lines
for n=1:length(indexRange)
    polar([fdArg1(n),fdArg2(n)],[fdMag1(n),fdMag2(n)],'g');
end;
hold off;

% % Log-magnitude scale
subplot(1,2,2);
polar(fdArg1,50*log10(1+99*fdMag1/fdMaxMag),'bo');
hold on;
polar(fdArg2,50*log10(1+99*fdMag2/fdMaxMag),'ro');
text=sprintf('FDs for %d\\leqn\\leq%d (Normalised Log Magnitudes \\leq100)',pmin,pmax);
title(text);

% Error lines
for n=1:length(indexRange)
    polar([fdArg1(n),fdArg2(n)], ...
        50*log10(1+99*[fdMag1(n),fdMag2(n)]/fdMaxMag),'g');
end;
hold off;




