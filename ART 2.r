rm(list=ls())
require(dtwclust)
require(TSclust)
require(TSdist)
require(dtw)
require(clusterSim)
require(cluster)
require(TTR)
require(RSNNS)

int.polation = 100
win.size = 3
cluster.try = 3


#Learn functions
p.l = 0
a.l = 25
b.l = 25
c.l = .10
theta.l = .10


#update function
p = 0
a = 150
b = 150
c = .10
theta = .20

#initialization function
d = .9
m = 3.5

max.f2 = 20
max.int = 150

paste.element = paste("_p-", p, "_a-", a, "_b-", b, "_c-", c, "_theta-", theta,"_count-", max.f2, sep="")

print(paste.element)

data.name = "Data_Matrix_ALL.csv"
NN.name1 = paste("NN_ALL_ASSIGN", paste.element, ".txt", sep="")
NN.name2 = paste("NN_ALL_ASSIGN_COUNT", paste.element, ".txt", sep="")
name.clustering = paste("IMAGES_FOR_NN_", paste.element)








set.seed(12347)
rm(model)


data.file = data.name
data = read.csv(data.file, header=TRUE)

for (i in 1:length((data[1,]))){
  f = data[,i][1:length(which(!is.na(data[,i])))]
  data.norm <-  data.Normalization(f,type="n4",normalization="column")
  dist.f = length(data[,i]) - length(which(!is.na(data[,i])))
  data.norm = c(data.norm, matrix(data=NA,nrow=1,ncol=dist.f))
  data[,i] = data.norm
}

sample.size = length((data[1,]))
data.new = matrix(0, ncol = sample.size, nrow = int.polation)


for (i in 1:sample.size){
  f = data[,i][1:length(which(!is.na(data[,i])))]
  
  data.intPol = approx(seq(1,length(f),1), y = f, method="linear", n=int.polation,rule = 3, f = 1, ties = mean)$y
  
  data.new[,i] = data.intPol
}

data.new = t(data.new)


FuncParams = c(p, a, b, c, theta)
learn.FuncParams = c(p.l, a.l, b.l, c.l, theta.l)
init.function = c(d,m)
model = art2(data.new, learnFunc = "ART2",maxit = max.int, f2Units = max.f2, initFuncParams = init.function,learnFuncParams = learn.FuncParams, updateFunc = "ART2_Stable", updateFuncParams = FuncParams, shufflePatterns = TRUE)


predictions <- predict(model, data.new)
#predictions


rm(table.NN1, table.NN2)

for (i in 1){
  for (j in 1:length(predictions[1,])){
    if (predictions[i,j] > 0){
      table.NN1 = t(rbind(colnames(data)[1], j))
      next
    
  }
  }
}

for (i in 1:length(predictions[,1])){
  set = 0
  for (j in 1:length(predictions[i,])){
    if (j==length(predictions[i,])){
      if (predictions[i,j] == 0){
        if (set == 0){
          table.NN2 = t(rbind(colnames(data)[i], as.numeric(j)))
          table.NN1 = rbind(table.NN1, table.NN2)
        }
      }
    }
    if (predictions[i,j] > 0){
      table.NN2 = t(rbind(colnames(data)[i], as.numeric(j)))
      table.NN1 = rbind(table.NN1, table.NN2)
      set = 1
    next
    }

  }
}

count.list = sum(table.NN1[,2] == 1)

for (i in seq(2,max(as.numeric(table.NN1[,2])))){
  count.list = rbind(count.list, sum(table.NN1[,2] == i))
}


table.NN1 = matrix(table.NN1,ncol = 2, dimnames = NULL)

write.matrix(table.NN1, file =NN.name1)
write.matrix(count.list, file=NN.name2)







rm(cluster.list)
table = read.table(NN.name1, row.names=NULL)
count = read.table(NN.name2)

png(paste(name.clustering,".png"), width=1500, height=1000)

table = table[2:length(table[,1]),]

roundUpNice <- function(x, nice=c(1,2,4,6,8,10)) {
    if(length(x) != 1) stop("'x' must be of length 1")
    10^floor(log10(x)) * nice[[which(x <= 10^floor(log10(x)) * nice)[[1]]]]
}

par(mfrow=c(2,roundUpNice(max(table[,2]))/2))

print(roundUpNice(max(table[,2])))


data = read.csv(data.file, header=TRUE)


for (i in 1:length((data[1,]))){
  f = data[,i][1:length(which(!is.na(data[,i])))]
  data.norm <-  data.Normalization(f,type="n4",normalization="column")
  dist.f = length(data[,i]) - length(which(!is.na(data[,i])))
  data.norm = c(data.norm, matrix(data=NA,nrow=1,ncol=dist.f))
  data[,i] = data.norm
}

for (x in seq(1,max(table[,2]),1)){
  cluster.number = x
  clear.check = 1

  for (i in seq(1:length(table[,1]))){
    if (cluster.number == table[i,2]){
      if (clear.check != 1){
        G1 = data[,i][1:length(which(!is.na(data[,i])))]
        G1
        c = c(0)
        
        G1 = c(c,G1)
        G1 = c(G1,c)
        X1 = seq(1,length(G1),1)
        G1 = approx(seq(1,length(G1),1), y = G1, method="linear", n=int.polation,rule = 3, f = 1, ties = mean)
        cluster.list = cbind(cluster.list,G1$y)
      }
    }
      if (clear.check == 1){
        G1 = data[,i][1:length(which(!is.na(data[,i])))]
        c = c(0)
        
        G1 = c(c,G1)
        G1 = c(G1,c)
        X1 = seq(1,length(G1),1)
        G1 = approx(seq(1,length(G1),1), y = G1, method="linear", n=int.polation,rule = 3, f = 1, ties = mean)
        cluster.list = matrix(G1$y)
        clear.check = 2
      }
    }

  
#plot(cluster.list[,2],type="l",col="blue")
#points(cluster.list[,3],type="l",col="red")
  
DBA = DBA(t(cluster.list),step=symmetric1, keep=TRUE,window.type=slantedBandWindow,window.size=win.size)


DBA = SMA(DBA,n=3)


  
plot(seq(1,length(DBA),1),main=paste("Cluster ",cluster.number),DBA,type="l",col="blue",xlab=paste("Number of Sets:  ",count[x,]), ylab="Normalized Fluorescence Intensity",cex.lab=1)
  #lines(G2.x,G2.y,col="red")
}

dev.off()
