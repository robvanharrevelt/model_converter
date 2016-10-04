library(microbenchmark)
library(compiler)

source("huge_islm.R")

y <- numeric(14000)
x <- numeric(4000)
d <- numeric(6000)
a <- numeric(8000)
fix <- numeric(8000)
fixval <- numeric(8000)
p <- numeric(14)

x[2001:4000] <- 0.2
p[] <- 10

system.time(y_new <- run_model_r(y, x, d, a, fix, fixval, p))
system.time(y_new <- run_model_r(y, x, d, a, fix, fixval, p))
print(sum(y_new))

t <- microbenchmark(y_new <- run_model_r(y, x, d, a, fix, fixval, p))
print(t)
print(sum(y_new))

system.time(run_model_r2 <- cmpfun(run_model_r, options = list(optimize =  0)))
print("bytecode generated")

t <- microbenchmark(y_new <- run_model_r2(y, x, d, a, fix, fixval, p))
print(t)

print(sum(y_new))

system.time(run_model_r3 <- cmpfun(run_model_r, options = list(optimize =  1)))
print("bytecode generated")

t <- microbenchmark(y_new <- run_model_r3(y, x, d, a, fix, fixval, p))
print(t)

print(sum(y_new))

system.time(run_model_r4 <- cmpfun(run_model_r, options = list(optimize =  2)))
print("bytecode generated")

t <- microbenchmark(y_new <- run_model_r4(y, x, d, a, fix, fixval, p))
print(t)

system.time(run_model_r5 <- cmpfun(run_model_r, options = list(optimize =  3)))
print("bytecode generated")

t <- microbenchmark(y_new <- run_model_r5(y, x, d, a, fix, fixval, p))
print(t)
