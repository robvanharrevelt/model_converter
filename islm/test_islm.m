y = zeros(7, 1);
y_in = zeros(7, 1);
x = zeros(2, 1);
d = zeros(3, 1);
a = zeros(4, 1);
fix = zeros(4, 1 );
fixval = zeros(4, 1);
p = 10 * ones(14, 1);

x(2) = 0.2;

tic()
y = islm(y_in, x, d, a, fix, fixval, p);
toc()
tic()
y = islm(y_in, x, d, a, fix, fixval, p);
toc()

tic()
for i = 1:1e3
y = islm(y_in, x, d, a, fix, fixval, p);
end
toc()
sum(y)
