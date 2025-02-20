function z = fdcurve( c,t,kmin,kmax )
% Compute the complex curve z(t) specified by its Fourier Descriptors (FDs).
%
% c     Column vector of FDs
% t     [Optional] Column vector of parameter values at which to evaluate the curve
% kmin  [Optional] Smallest FD index, stored in c(1)
% kmax  [Optional] Largest FD index, stored in c(kmax-kmin+1)
%
% fdcurve(c) computes z(t) at 100 equally spaced points for t in [0,1)
% and assumes default values for kmin & kmax.
%
% fdcurve(c,t) computes z(t) at the points specified in the vector t, and
% assumes default values for kmin & kmax.
%
% fdcurve(c,t,kmin,kmax) computes z(t) at the points specified in the vector t

% Called as fdcurve(c) or fdcurve(c,t)
if nargin < 3
    nFDs=length(c);
    kmin=-floor(nFDs/2);
    kmax=nFDs+kmin-1;
end
    
% Called as fdcurve(c)
if nargin == 1
    N=100;
    t=(0:N-1)'/N;
end

% Compute curve
k=[kmin:kmax]';
z=exp(1i*2*pi*t(:)*k')*c(:);
