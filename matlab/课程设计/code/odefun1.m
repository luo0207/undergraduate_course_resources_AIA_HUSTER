function dydt = odefun1(t,y,rx,px,ry,py,a,b)%正规战的仿真模型
dydt = zeros(2,1);
dydt(1) = -ry*py*y(2)-a*y(1);
dydt(2) = -rx*px*y(1)-b*y(2);
end