y = zeros(140, 1);
y_in = zeros(140, 1);
x = zeros(40, 1);
d = zeros(60, 1);
a = zeros(80, 1);
fix = zeros(80, 1 );
fixval = zeros(80, 1);
p = 10 * ones(14, 1);

x(21:40) = 0.2;

tic()
y = intermediate_islm(y_in, x, d, a, fix, fixval, p);
toc()
tic()
y = intermediate_islm(y_in, x, d, a, fix, fixval, p);
toc()

tic()
for i = 1:1e3
y = intermediate_islm(y_in, x, d, a, fix, fixval, p);
end
toc()
sum(y)
