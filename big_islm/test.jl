include("big_islm.jl")

println("functie ingelezen")

y = zeros(3500)
y_in = zeros(3500)
x = zeros(1000)
d = zeros(1500)
a = zeros(2000)
fix = falses(2000)
fixval = zeros(2000)
p = 10 * ones(14)

x[500:1000] = 0.2

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
