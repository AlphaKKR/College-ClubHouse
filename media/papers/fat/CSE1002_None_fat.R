rm(list=ls())
library(lubridate)
library(stringr)
setwd('C:/Soiram/freelance/Aleksey')

my_data <- read.delim("alexishikula.txt",sep = "|",header = FALSE)
var1<-my_data[,1]
ndata<-length(var1)
date_str<-c()
time_str<-c()
user<-c()
date_time_str<-c()

for(i in 1:ndata)
{
  current<-var1[i]
  split_current<-unlist(strsplit(current, " "))
  split_current<-trimws(x = split_current)
  date_str<-c(date_str,split_current[1])
  time_str<-c(time_str,split_current[2])
  user<-c(user,split_current[3])
  date_time_str<-c(date_time_str,paste(split_current[1]," ",split_current[2]))
}

var5<-my_data[,5]

start_block<-c()
end_block<-c()

for(i in 1:ndata)
{
  current<-var5[i]
  split_current<-unlist(strsplit(current, "-"))
  split_current<-trimws(x = split_current)
  start_block<-c(start_block,split_current[1])
  end_block<-c(end_block,split_current[2])
}
my_data[,2]<-trimws(x = my_data[,2])
my_data[,3]<-trimws(x = my_data[,3])
my_data[,4]<-trimws(x = my_data[,4])


date_time<-as.POSIXct(date_time_str)
year_dat<-year(date_time)
month_dat<-month(date_time)
day_dat<-day(date_time)
hour_dat<-hour(date_time)
min_dat<-minute(date_time)
sec_dat<-second(date_time)
frac_sec<-sec_dat-floor(sec_dat)
sec_dat<-floor(sec_dat)



data<-cbind(date_time_str,date_str,year_dat,month_dat,day_dat,hour_dat,min_dat,sec_dat,frac_sec,
            user,my_data[,2],my_data[,3],my_data[,4],start_block,end_block)

#date_time<-date_time[order(date_time,decreasing = FALSE)]
data<-data[order(as.integer(data[,3]),as.integer(data[,4]),
                 as.integer(data[,5]),as.integer(data[,6]),
                 as.integer(data[,7]),as.integer(data[,8]),
                 as.numeric(data[,9]),decreasing = FALSE),]

starting_date<-as.numeric(ymd(data[1,2]))
day_acum<-c()
for (i in 1:ndata)
{
  date_i<-as.numeric(as.Date(data[i,2]))
  hour_i<-as.numeric(data[i,6])/24
  min_i<-as.numeric(data[i,7])/(24*60)
  sec_i<-(as.numeric(data[i,8])+as.numeric(data[i,9]))/(24*60*60)
  time_record_i<-date_i+hour_i+min_i+sec_i
  time_record_i<-time_record_i-starting_date
  day_acum<-c(day_acum,time_record_i)
}

Nt<-seq(1:ndata)
min_acum<-day_acum*24*60

inter_min<-min_acum[1]

for ( i in 2:ndata)
{
  delta_i<-min_acum[i]-min_acum[i-1]
  inter_min<-c(inter_min,delta_i)
}

data<-cbind(data[,1],Nt,min_acum,inter_min,data[,2:15])

data<-as.data.frame(data)

library(keras)
library(tensorflow)
library(ggplot2)
library(stats)
library(readr)
library(dplyr)
library(forecast)
library(Metrics)

title<-paste("Starting date ", data$date_str[1], "At 00:00")
data$Nt<-as.integer(data$Nt)
data$min_acum<-as.numeric(data$min_acum)
ggplot(data, aes(x=data$min_acum, y = data$Nt)) + geom_line()+
  xlab('Time in minutes')+
  ylab('Orders')+
  ggtitle(title)+theme(plot.title = element_text(hjust = 0.5))

#predictors

X_serie<-as.numeric(data[,12])
X_lag1<-as.numeric(data[-1,12])
X<-cbind(X_serie[1:(ndata-1)],X_lag1)
nX<-ncol(X)
X<-X[5000:nX,]
ptrain<-0.95

n_X<-nrow(X)

n_train<-floor(n_X*ptrain)

train<-X[1:n_train,]

test<-X[(n_train+1):n_X,]



scale_data <- function(train, test, feature_range = c(0,1)) {
  x = train
  fr_min = feature_range[1]
  fr_max = feature_range[2]
  std_train = (x - min(x)) / (max(x) - min(x))
  std_test = (test - min(x)) / (max(x) - min(x))
  
  scaled_train = std_train * (fr_max - fr_min) + fr_min
  scaled_test = std_test * (fr_max - fr_min) + fr_min
  
  return( list(scaled_train = scaled_train, scaled_test = scaled_test ,scaler= c(min =min(x), max = max(x))) )
}


#Function to reverse scale data for prediction
reverse_scaling <- function(scaled, scaler, feature_range = c(0,1)) {
  min = scaler[1]
  max = scaler[2]
  t = length(scaled)
  mins = feature_range[1]
  maxs = feature_range[2]
  inverted_dfs = numeric(t)
  
  for(i in 1:t) {
    X = (scaled[i] - mins) / (maxs - mins)
    rawValues = X * (max - min) + min
    inverted_dfs[i] <- rawValues
  }
  return(inverted_dfs)
}


Scaled <- scale_data(train, test, c(-1,1))

x_train <- Scaled$scaled_train[,1]
y_train <- Scaled$scaled_train[,2]

x_test <- Scaled$scaled_test[,1]
y_test <- Scaled$scaled_test[,2]



dim(x_train) <- c(length(x_train), 1, 1)


# specify required arguments
X_shape2 = dim(x_train)[2]
X_shape3 = dim(x_train)[3]
batch_size = 1                
units = 1                     

model <- keras_model_sequential() 
model%>%
  layer_lstm(units, batch_input_shape = c(batch_size, X_shape2, X_shape3), stateful= TRUE)%>%
  layer_dense(units = 1)

model %>% compile(
  loss = 'mean_squared_error',
  optimizer = optimizer_adam( lr= 0.02, decay = 1e-6 ),  
  metrics = c('accuracy')
)

summary(model)

Epochs = 50   
for(i in 1:Epochs ){
  model %>% fit(x_train, y_train, epochs=1, batch_size=batch_size, verbose=1, shuffle=FALSE)
  model %>% reset_states()
}

L = length(x_test)
scaler = Scaled$scaler
predictions = numeric(L)



for(i in 1:L){
  X = x_test[i]
  dim(X) = c(1,1,1)
  yhat = model %>% predict(X, batch_size=batch_size)
  # invert scaling
  yhat = reverse_scaling(yhat, scaler,  c(-1, 1))
  # store
  predictions[i] <- yhat
}

compare<-cbind(test,predictions)
View(compare)
