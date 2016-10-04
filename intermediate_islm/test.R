library(microbenchmark)
library(compiler)

system.time(
source("intermediate_islm.R")
)

y <- numeric(140)
x <- numeric(40)
d <- numeric(60)
a <- numeric(80)
fix <- numeric(80)
fixval <- numeric(80)
p <- numeric(14)

x[21:40] <- 0.2
p[] <- 10

system.time(y_new <- run_model_r(y, x, d, a, fix, fixval, p))

t <- microbenchmark(y_new <- run_model_r(y, x, d, a, fix, fixval, p))
print(t)
print(sum(y_new))

system.time(run_model_r2 <- cmpfun(run_model_r))

t <- microbenchmark(y_new <- run_model_r2(y, x, d, a, fix, fixval, p))
print(t)

print(sum(y_new))
