function compareFDs( fd1,fd2,N );
% Plot two curves with Fourier Descriptors (FDs) in fd1 & fd2 using N points
% around the perimeter. Also display the FD magnitudes and a polar plot of 
% FD values on a log-polar plot.
%
% plotFDs( fd1,fd2 )   Plot the FDs with 100 perimeter samples
%
% plotFDs( fd1,fd2,N ) Plot the FDs with N perimeter samples

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

if nargin < 3
    N=100;
end;

% Plot curve
figure;
subplot(2,2,[1,3]);
t=(0:N-1)'/N;

z1=fdcurve(fd1,t);
plot(z1,curveLineSpec1);
axis equal;
hold on;

z2=fdcurve(fd2,t);
plot(z2,curveLineSpec2);

plot(real(z1(1)),imag(z1(1)),startLineSpec1);
plot(real(z2(1)),imag(z2(1)),startLineSpec2);

hold off;
text=sprintf('Curve (%d FDs, %d Boundary Samples)',nFDs,N);
title(text);
legend('Curve 1','Curve 2','Start Position');

% Plot FD magnitudes
subplot(2,2,2);
stem([minIndex:maxIndex],abs(fd1),'b');
hold on;
stem([minIndex:maxIndex],abs(fd2),'r');
hold off;
text=sprintf('FD Magnitudes for %d\\leqn\\leq%d',minIndex,maxIndex);
title(text);
xlim([minIndex,-minIndex]);
xlabel('FD Index');
ylabel('FD Magnitide');

% Plot FDs in polar form
subplot(2,2,4);
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



