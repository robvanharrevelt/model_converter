y_in = zeros(14000, 1);
x = zeros(4000, 1);
d = zeros(6000, 1);
a = zeros(8000, 1);
fix = zeros(8000, 1 );
fixval = zeros(8000, 1);
p = 10 * ones(14, 1);

x(2001:4000) = 0.2;

tic()
y = huge_islm(y_in, x, d, a, fix, fixval, p);
toc()
tic()
y = huge_islm(y_in, x, d, a, fix, fixval, p);
toc()

tic()
for i = 1:1e2
y = huge_islm(y_in, x, d, a, fix, fixval, p);
end
toc()
sum(y)
