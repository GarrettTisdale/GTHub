rm(list=ls())

library(rnn)
require(ggplot2)
set.seed(45)


train = read.csv("training_set_diana.csv", header = TRUE)
test = read.csv("test_set_diana.csv", header = TRUE)

dc1_p = train[,4]
dc2_p = train[,5]


#Getting and working with data
data.temp = rbind(dc1_p, dc2_p)
data.combined = rbind(dc1_p, dc2_p, seq(1, ncol(data.temp), by=1))
data = data.frame(dc1_p=data.combined[1,], dc2_p=data.combined[2,], tau=data.combined[3,])


N = ncol(data.temp)


df <- data.frame(tau=seq(1, ncol(data.temp), by=1), dc1_p=data.combined[1,], dc2_p=data.combined[2,])
# plot
ggplot(data = df, aes(x=tau, y=dc1_p))+ geom_line(colour="Green")
ggplot(data = df, aes(x=tau, y=dc2_p))+ geom_line(colour="Red")



#Correlation function
z = (((fft(((Conj(fft(dc1_p)) * fft(dc2_p))), inverse=TRUE))/N) / (mean(dc1_p) * mean(dc2_p))) - 1

df <- data.frame(tau=seq(1, ncol(data.temp), by=1), dc1_p=data.combined[1,], dc2_p=data.combined[2,], correlation=Re(z))
ggplot(data = df, aes(x=tau, y=correlation))+ geom_line(colour="blue")


#Creating inputs for model
datax.combined = rbind(dc2_p)
datax1.combined = rbind(dc1_p)
datax2.combined =rbind(seq(1, ncol(data.temp), by=1))

#Normailize
datax.combined = (datax.combined - min(datax.combined)) / (max(datax.combined) - min(datax.combined))
datax1.combined = (datax1.combined - min(datax1.combined)) / (max(datax1.combined) - min(datax1.combined))
datax2.combined = (datax2.combined - min(datax2.combined)) / (max(datax2.combined) - min(datax2.combined))

datax3.combined = rbind(datax.combined)

correlation = (Re(z) - min(Re(z))) / (max(Re(z)) - min(Re(z)))
datay.combined = rbind(correlation)

bindx = rbind(datax3.combined)
bindy = rbind(datay.combined)

X = bindx
Y = bindy


Training
rnn1_3 = trainr(Y = Y,
              X = X,
              learningrate = .01,
              hidden_dim = 12,
              numepochs = 3000)


plot(colMeans(rnn1_3$error),type='l',
     xlab='epoch',
     ylab='errors'                  )


#Writing data to files
# trainingData = t(rbind(datax1.combined, X,Y))
# write.csv(trainingData, file="training_data_normalized.csv")
# 
# 
# datax.combined = rbind(dc2_p)
# datax1.combined = rbind(dc1_p)
# datax2.combined =rbind(seq(1, ncol(data.temp), by=1))
# correlation = Re(z)
# 
# bindx = rbind(datax.combined)
# bindy = rbind(datay.combined)
# 
# X = bindx
# Y = bindy
# 
# trainingData = t(rbind(datax1.combined, X, correlation))
# write.csv(trainingData, file="training_data_unnormalized.csv")

#TESTING
dc1_p_test = test[,4]
dc2_p_test = test[,5]


#Working with test data
data.temp_test = rbind(dc1_p_test, dc2_p_test)
data.combined_test = rbind(dc1_p_test, dc2_p_test, seq(1, ncol(data.temp_test), by=1))
data_test = data.frame(dc1_p=data.combined_test[1,], dc2_p=data.combined_test[2,], tau=data.combined_test[3,])


N_test = ncol(data.temp_test)


df_test <- data.frame(tau=seq(1, ncol(data.temp_test), by=1), dc1_p=data.combined_test[1,], dc2_p=data.combined_test[2,])
ggplot(data = df_test, aes(x=tau, y=dc1_p))+ geom_line(colour="Green")
ggplot(data = df_test, aes(x=tau, y=dc2_p))+ geom_line(colour="Red")



#Test Correlation funciton
z_test = (((fft(((Conj(fft(dc1_p_test)) * fft(dc2_p_test))), inverse=TRUE))/N_test) / (mean(dc1_p_test) * mean(dc2_p_test))) - 1

df_test <- data.frame(tau=seq(1, ncol(data.temp_test), by=1), dc1_p=data.combined_test[1,], dc2_p=data.combined_test[2,], correlation=Re(z_test))
ggplot(data = df_test, aes(x=tau, y=correlation))+ geom_line(colour="blue")



#Setting up input data for predict
datax.combined_test = rbind(dc2_p_test)
datax1.combined_test = rbind(dc1_p_test)
datax2.combined_test =rbind(seq(1, ncol(data.temp_test), by=1))

datax.combined_test = (datax.combined_test - min(datax.combined_test)) / (max(datax.combined_test) - min(datax.combined_test))
datax2.combined_test = (datax2.combined_test - min(datax2.combined_test)) / (max(datax2.combined_test) - min(datax2.combined_test))

datax3.combined_test = rbind(datax.combined_test, datax2.combined_test)

dataz_test = (Re(z_test) - min(Re(z_test))) / (max(Re(z_test)) - min(Re(z_test)))

datay.combined_test = rbind(dataz_test, datax2.combined_test)


bindx_test = rbind(datax3.combined_test)
bindy_test = rbind(datay.combined_test)

X_test = bindx_test
Y_test = bindy_test


#The predict_rnn did not work for what ever reason but this should be the same command
predict_values = predictr(rnn1_3, X_test)

df_test2 <- data.frame(tau=predict_values[2,], dc1_p=data.combined_test[1,], dc2_p=data.combined_test[2,], correlation=predict_values[1,])


ggplot(data = df_test2, aes(x=tau, y=correlation))+ geom_line(colour="Red")

