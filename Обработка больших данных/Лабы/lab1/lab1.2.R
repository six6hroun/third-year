df <- data.frame(var1=c(1,2,3), var2=c(4,5,6), var3=c(7,8,0), var4=c(9,10,11), row.names=c("case1", "case2", "case3"))

print (df["case1", c("var1", "var2", "var3")])

print (df["case3", df["case3", ] < 8])

print (colnames(df)[c(2, 4)])

df$Y <- c(-10, 0, 11)
print(df)

print (df <- df[-2, ])

df$var2 <- df$var2^3

print(df)