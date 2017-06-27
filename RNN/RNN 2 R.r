rm(list=ls())

library(rnn)
require(ggplot2)
require(astsa)
rdata = read.csv("training_data_unnormalized_ccf.csv")

set.seed(45)


dc1_p = rdata[,2][1:1000]
dc2_p = rdata[,3][1:1000]
Crco = rdata[,4]

dc1_p.norm = (dc1_p - min(dc1_p)) / (max(dc1_p) - min(dc1_p))
dc2_p.norm = (dc2_p - min(dc2_p)) / (max(dc2_p) - min(dc2_p))

X = rbind(dc1_p.norm)
Y = rbind(Crco)


# #Training
# rnn1_1 = trainr(Y = Y,
#                 X = X,
#                 learningrate = .1,
#                 hidden_dim = 2,
#                 numepochs = 3000)
# 
# 
# plot(colMeans(rnn1_1$error),type='l',
#      xlab='epoch',
#      ylab='errors'                  )


X = rbind(dc1_p.norm)
Y = rbind(Crco)
rnn1_2 = trainr(Y = Y,
                X = X,
                learningrate = .01,
                hidden_dim = 2,
                numepochs = 3000)


plot(colMeans(rnn1_2$error),type='l',
     xlab='epoch',
     ylab='errors'                  )




