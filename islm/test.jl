include("islm.jl")

y = zeros(7)
y_in = zeros(7)
x = zeros(2)
d = zeros(3)
a = zeros(4)
fix = falses(4)
fixval = zeros(4)
p = 10 * ones(14)

x[2] = 0.2

# the results of the first call of @time should not be taken seriously
@time (run_model_julia(y, y_in, x, d, a, fix, fixval, p))

@time (run_model_julia(y, y_in, x, d, a, fix, fixval, p))

@time (for i = 1:1e6
           run_model_julia(y, y_in, x, d, a, fix, fixval, p)
       end)
println(sum(y))

tic()
for i = 1:1e6
    run_model_julia(y, y_in, x, d, a, fix, fixval, p)
end
toc()
