function s = arcLength( c,t,kmin,kmax )
% Compute the arc length over [0,t] for the general FDs c.
%
% c     Column vector of FDs
% t     [Optional] Parameter value up to which the arc length is calculated
% kmin  [Optional] Smallest FD index, stored in c(1)
% kmax  [Optional] Largest FD index, stored in c(kmax-kmin+1)
%
% arcLength(c) computes the perimeter over [0,1) and assumes default values
% for kmin & kmax.
%
% arcLength(c,t) computes the arc length over [0,t) and assumes default
% values for kmin & kmax.
%
% arcLength(c,t,kmin,kmax) computes the arc length over [0,t).

% Called as arcLength(c) or arcLength(c,t)
if nargin < 3
    nFDs=length(c);
    kmin=-floor(nFDs/2);
    kmax=nFDs+kmin-1;
end;

% Called as arcLength(c)
if nargin == 1
    t=1;
end;

% Define modulus of curve speed
k=[kmin:kmax]';
d=i*2*pi*c.*k;
dzdt=@(u) abs(exp(i*2*pi*u'*k')*d)';

% Compute arc length
s=integral(dzdt,0,t);
%s=quadgk(dzdt,0,t);
    

