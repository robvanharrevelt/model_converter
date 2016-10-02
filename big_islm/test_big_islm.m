y_in = zeros(3500, 1);
x = zeros(1000, 1);
d = zeros(1500, 1);
a = zeros(2000, 1);
fix = zeros(2000, 1 );
fixval = zeros(2000, 1);
p = 10 * ones(14, 1);

x(500:1000) = 0.2;

tic()
y = big_islm(y_in, x, d, a, fix, fixval, p);
toc()
tic()
y = big_islm(y_in, x, d, a, fix, fixval, p);
toc()

tic()
for i = 1:1e2
y = big_islm(y_in, x, d, a, fix, fixval, p);
end
toc()
sum(y)
