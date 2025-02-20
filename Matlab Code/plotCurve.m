function plotCurve( fd,N );
% Plot the curve with Fourier Descriptors (FDs) in fd using N points around
% the perimeter.
%
% plotCurve( fd )   Plot the FDs with 100 perimeter samples
%
% plotCurve( fd,N ) Plot the FDs with N perimeter samples

nFDs=length(fd);
minIndex=-floor(nFDs/2);
maxIndex=minIndex+nFDs-1;
curveLineSpec='-bo';
startLineSpec='rs';

if nargin==1
    N=100;
end;

% Plot curve
%figure;
t=(0:N-1)'/N;
z=fdcurve(fd,t);
plot(z,curveLineSpec);
axis equal;
hold on;
plot(real(z(1)),imag(z(1)),startLineSpec);
hold off;
text=sprintf('Curve (%d FDs, %d Boundary Samples)',nFDs,N);
title(text);