library(microbenchmark)
library(compiler)

source("islm.R")

y <- numeric(7)
x <- numeric(2)
d <- numeric(3)
a <- numeric(4)
fix <- numeric(4)
fixval <- numeric(4)
p <- numeric(14)

x[2] <- 0.2
p[] <- 10

t <- microbenchmark(y_new <- run_model_r(y, x, d, a, fix, fixval, p))
print(t)
print(y_new)

print(sum(y_new))

run_model_r2 <- cmpfun(run_model_r)

t <- microbenchmark(y_new <- run_model_r2(y, x, d, a, fix, fixval, p))
print(t)

print(sum(y_new))
