function t = invArcLength( c,s )
% Compute t given arc length position s and FDs c.
%
% c     Column vector of FDs
% s     Arc length position
%
% invArcLength(c,s) computes t such that arcLength(c,t) = s

% Use fzero to find t
t0=s/arcLengthLocal(c,1);
t=fzero( @(u) arcLengthLocal(c,u)-s,t0 );

end

function s = arcLengthLocal( c,t )

% Define curve speed
nFDs=length(c);
kmin=-floor(nFDs/2);
k=[kmin:nFDs+kmin-1]';
d=i*2*pi*c.*k;
dzdt=@(u) abs(exp(i*2*pi*u'*k')*d)';

% Compute arc length
s=integral(dzdt,0,t);
%s=quadgk(dzdt,0,t);

end




