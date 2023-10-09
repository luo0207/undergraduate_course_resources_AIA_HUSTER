function dydt = odefun2(t,y,rx,sx,ry,sy,a,b)%游击战的仿真模型
dydt = zeros(2,1);
dydt(1) = -ry*(sy/sx)*y(2)*y(1)-a*y(1);
dydt(2) = -rx*(sx/sy)*y(1)*y(2)-b*y(2);
end