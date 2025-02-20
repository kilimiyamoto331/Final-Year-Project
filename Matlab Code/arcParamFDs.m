function fds = arcParamFDs( fdt,N )
% Given the FD parameter fdt, parameterised by t in [0,1), return the 
% FDs for arc length parameterisation. N is the number of FDs to return.
% Note that changing to arc length parameterisation could theoretically 
% require an infinite number of new FDs. The default value for N is 64.

% Called as arcParamFDs( fdt )
if nargin == 1
    N=64;
end;

% Compute evenly spaced samples around the perimeter
s=(0:N-1)'/N*arcLength(fdt);
ts=zeros(size(s));
for n=1:length(s)
    ts(n)=invArcLength(fdt,s(n));
    %n
end; 

%ts=(0:N-1)'/N;

% Compute new FDs
z=fdcurve(fdt,ts);
fds=fftshift(fft(z))/N;

% DEBUG
% figure;
% plot(s,ts);
% title('Re-parameterisation Curve');
% text=sprintf('Arc-length (0\\leq s\\leq %.4f)',arcLength(fdt));
% xlabel(text);
% ylabel('Base parameter (0\leq t\leq 1)');




