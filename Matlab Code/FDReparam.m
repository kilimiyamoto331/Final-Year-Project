%% Fourier Descriptor Study of the Ellipse

%% Ellipse parameterisation

% Setup t-parameterisation values
N=64;                                % Number of points along perimeter
kmin=-1;                             % Index range for FDs   
kmax=+1;
c=100*[-0.5,0,-1.5i]';               % FDs

% Compute arc-length of ellipse
totalLength=arcLengthE(c);

% Generate evenly spaced samples of parameters
t=(0:N-1)'/N;                % t in [0,1)
s=(0:N-1)'/N*totalLength;    % s in [0,totalLength)

% Given s, find corresponding t-values
ts=zeros(size(s));
for n=1:size(ts,1)
    ts(n)=invArcLengthE(c,s(n));
    %n
end

% Display re-parameterisation curve
figure;
plot(s,ts);
title('Re-parameterisation Curve');
xlabel('Arc-length (0\leq s\leq P)');
ylabel('Base parameter (0\leq t\leq 1)');

%% Create ellipses and FDs

% t-space curve and FDs
zt=c(1)*exp(-1i*2*pi*t)+c(2)+c(3)*exp(1i*2*pi*t);
fdt=fftshift(fft(zt))/N;

% s-space curve and FDs
zs=c(1)*exp(-1i*2*pi*ts)+c(2)+c(3)*exp(1i*2*pi*ts);
fds=fftshift(fft(zs))/N;

% Plot ellipses
figure;
plot(real(zt),imag(zt),'x',real(zs),imag(zs),'ro');
axis equal

% Annotation
title('Ellipse Samples');
legend('t parameter','s parameter');

%% Plot Fourier descriptors

% t-space FDs
figure;
stem(-floor(N/2):floor(N/2)-1,abs(fdt),'r')
hold on;

% s-space FDs
stem(-floor(N/2):floor(N/2)-1,abs(fds),'g')
hold off;

% Annotation
title('Fourier Descriptors');
xlim([-floor(N/2),floor(N/2)]);
xlabel('Fourier index (n)');
ylabel('FD magnitide');
legend('t parameter','s parameter');

%% Plot new curves based on FDs

% Generate curve, first and second-derivative
zs_new=fdcurve(fds,t);
zds_new=fdtangent(fds,t);
zd2s_new=fdnormal(fds,t);

% Plot curve
figure;
plot(real(zs_new),imag(zs_new));
axis equal;
hold on;

% Plot derivatives
quiver(real(zs_new),imag(zs_new),real(zds_new),imag(zds_new));
quiver(real(zs_new),imag(zs_new),real(zd2s_new),imag(zd2s_new));
hold off;

% Annotation
title('Reconstructed ellipse: z(s), z''(s), z''''(s)');
legend('z(s)','z''(s)','z''''(s)') ;

% % Plot speed curve
% figure;
% plot(s,abs(zds_new)/abs(zds_new(1)));
% ylim([0 1.1]);
% 
% % Annotation
% title('Unit Speed Curve');
% xlabel('Arc-length (s)');
% ylabel('Speed |z''(s)|');

%% Effect of sampling on FDs and curve errors

% Compute approximate extent of ellipse
curveExtent=2*(abs(c(1))+abs(c(3)));

% Over-sample if necessary to "catch" every pixel
sampleCount=5.50*curveExtent;

% Compute integer samples
zSamples=fdcurve(fds,(0:sampleCount-1)'/sampleCount);
zCoords=round(zSamples);

% Note on modulo arithmetic below:
%   To cycle n from 0 to M-1 use mod(n,M)
%   but to cycle n from 1 to M use mod(n-1,M)+1

% Prune repeated samples
nCoords=1;
zCoordsPruned=zeros(size(zCoords));
zCoordsPruned(1)=zCoords(1);
for n=2:length(zCoords)
    if zCoords(n)~=zCoords(n-1)
        nCoords=nCoords+1;
        zCoordsPruned(nCoords)=zCoords(n);
    end
end
if zCoordsPruned(nCoords)==zCoordsPruned(1)
    nCoords=nCoords-1;
end
disp(sprintf('%d coordinates trimmed',length(zCoords)-nCoords));
zCoords=zCoordsPruned(1:nCoords);
clear zCoordsPruned;

% Prune 4-connected pixels
% nCoords=1;
% M=size(zCoords,1);
% xCoords=real(zCoords);
% yCoords=imag(zCoords);
% for n=1:size(zCoords,1)
%     if (xCoords(n)~=xCoords(mod(n-1-1,M)+1) || yCoords(n)~=yCoords(mod(n+1-1,M)+1)) && ...
%        (xCoords(n)~=xCoords(mod(n+1-1,M)+1) || yCoords(n)~=yCoords(mod(n-1-1,M)+1))
%         nCoords=nCoords+1;
%         zCoordsPruned(nCoords)=zCoords(n);
%     else
%         xCoords(n)=NaN;
%         yCoords(n)=NaN;
%     end;
% end;    
% zCoords=zCoordsPruned(1:nCoords);
% clear xCoords yCoords;

% Create arc-length samples and curve
t=(0:nCoords-1)'/nCoords;
zSamples=fdcurve(fds,t);

% Plot curve
figure;
plot(real(zSamples),imag(zSamples),real(zCoords),imag(zCoords),'+');
axis equal;
hold on;

% Plot location of s=0, and first integer sample location
plot(real(zSamples(1)),imag(zSamples(1)),'ro');
plot(real(zCoords(1)),imag(zCoords(1)),'go');

% Plot errors between exact curve samples and integer samples
for n=1:size(zCoords,1)
    plot([real(zSamples(n)),real(zCoords(n))],[imag(zSamples(n)),imag(zCoords(n))],'r');
end
hold off;

% % Compute approximate accumulated arc length
% zSamplesArc=cumsum(abs(zSamples-circshift(zSamples,1)));
% zCoordsArc=cumsum(abs(zCoords-circshift(zCoords,1)));
% 
% % Plot accumulated arc length
% figure;
% plot(zSamplesArc,'r');
% hold on;
% 
% plot(zCoordsArc,'b');
% hold off;
% 
% % Annotation
% title('Accumulated Arc Length');
% ylabel('Arc length');
% legend('Exact curve samples','Integer curve samples','Location','NorthWest'); 

% Compute FDs of both curves
fdSamples=fftshift(fft(zSamples))/nCoords;
fdCoords=fftshift(fft(zCoords))/nCoords;

% Plot FDs as magnitudes
pmin=-10;
pmax=+10;
plotRange=pmin:pmax;
minIndex=-floor(length(fdSamples)/2);
indexRange=plotRange-minIndex+1;

% Exact samples
figure;
stem(plotRange,abs(fdSamples(indexRange)),'r')
hold on;

% Integer samples
stem(plotRange,abs(fdCoords(indexRange)),'g')
hold off;

% Annotation
title('Fourier Descriptor Magnitudes');
xlim([pmin,pmax]);
xlabel('Fourier index (n)');
ylabel('FD magnitide');
legend('Exact Samples','Integer Samples');

% Plot FDs as vectors in C
pmin=-10;
pmax=+10;
plotRange=pmin:pmax;
minIndex=-floor(length(fdSamples)/2);
indexRange=plotRange-minIndex+1;

% Create polar vectors 
[fdSamplesArg,fdSamplesMag]=cart2pol(real(fdSamples(indexRange)),imag(fdSamples(indexRange)));
[fdCoordsArg,fdCoordsMag]=cart2pol(real(fdCoords(indexRange)),imag(fdCoords(indexRange)));

% Exact samples
figure;
polar(fdSamplesArg,log10(1+fdSamplesMag),'xb');
hold on;

% Integer samples
polar(fdCoordsArg,log10(1+fdCoordsMag),'+g');

% Error lines
for n=1:length(fdSamplesArg)
    polar([fdSamplesArg(n),fdCoordsArg(n)],log10(1+[fdSamplesMag(n),fdCoordsMag(n)]),'r');
end
hold off;

% Annotation
nFDs=length(zCoords);
deltaS=totalLength/nFDs;
s=sprintf('Fourier Descriptors (N=%d, \\Deltas=%.4f)',nFDs,deltaS);
title(s);
% xlim([pmin,pmax]);
% xlabel('Fourier index (n)');
% ylabel('FD magnitide');
legend('Exact Samples','Integer Samples','Error');