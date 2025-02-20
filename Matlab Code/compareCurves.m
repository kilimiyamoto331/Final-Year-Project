function compareCurves( fd1,fd2,N );
% Plot two curves with Fourier Descriptors (FDs) in fd1 & fd2 using N points
% around the perimeter.
%
% plotFDs( fd1,fd2 )   Plot the FDs with 100 perimeter samples
%
% plotFDs( fd1,fd2,N ) Plot the FDs with N perimeter samples

% Ensure FDs have the same length - pad as necessary
if length(fd1) == length(fd2)
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
startLineSpec1='gs';
curveLineSpec2='ro';
startLineSpec2='gs';

if nargin < 3
    N=100;
end;

% Plot curves
figure;
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

