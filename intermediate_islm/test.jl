include("intermediate_islm.jl")

y = zeros(140)
y_in = zeros(140)
x = zeros(40)
d = zeros(60)
a = zeros(80)
fix = falses(80)
fixval = zeros(80)
p = 10 * ones(14)

x[21:40] = 0.2

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
