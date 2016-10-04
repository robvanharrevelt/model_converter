include("big_islm.jl")

println("functie ingelezen")

y = zeros(14000)
y_in = zeros(14000)
x = zeros(4000)
d = zeros(6000)
a = zeros(8000)
fix = falses(8000)
fixval = zeros(8000)
p = 10 * ones(14)

x[2001:4000] = 0.2

@time (zzz = 1)

# the results of the first call of @time should not be taken seriously
@time (run_model_julia(y, y_in, x, d, a, fix, fixval, p))

@time (run_model_julia(y, y_in, x, d, a, fix, fixval, p))

@time (for i = 1:1000
           run_model_julia(y, y_in, x, d, a, fix, fixval, p)
       end)
println(sum(y))

tic()
for i = 1:1000
    run_model_julia(y, y_in, x, d, a, fix, fixval, p)
end
toc()
