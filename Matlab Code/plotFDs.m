function plotFDs( fd,N );
% Plot the curve with Fourier Descriptors (FDs) in fd using N points around
% the perimeter. Also display the FD magnitudes and a polar plot of FD
% values on a log-polar plot.
%
% plotFDs( fd )   Plot the FDs with 100 perimeter samples
%
% plotFDs( fd,N ) Plot the FDs with N perimeter samples

nFDs=length(fd);
minIndex=-floor(nFDs/2);
maxIndex=minIndex+nFDs-1;
curveLineSpec='-bo';
startLineSpec='rs';

if nargin==1
    N=100;
end

% Plot curve
figure;
subplot(2,2,[1,3]);
t=(0:N-1)'/N;
z=fdcurve(fd,t);
plot(z,curveLineSpec);
axis equal;
hold on;
plot(real(z(1)),imag(z(1)),startLineSpec);
hold off;
text=sprintf('Curve (%d FDs, %d Boundary Samples)',nFDs,N);
title(text);

% Plot FD magnitudes
subplot(2,2,2);
stem([minIndex:maxIndex],abs(fd));
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
[fdArg,fdMag]=cart2pol(real(fd(indexRange)),imag(fd(indexRange)));
fdMaxMag=max(fdMag);
polar(fdArg,50*log10(1+99*fdMag/fdMaxMag),'bo');
text=sprintf('FDs for %d\\leqn\\leq%d (Normalised Log Magnitudes \\leq100)',pmin,pmax);
title(text);

