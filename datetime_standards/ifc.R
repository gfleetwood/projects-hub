library(tidyverse)

# Function to 
reconstruct_date <- function(y, md){
    return(
        as.integer(Sys.Date() - as.Date(paste(y, md, sep = "-")))
    )
}

# A function to convert from a Gregorian date to an IFC one
ifc_date <- function(y, m_id, m_name, ddelta, short = 1){
    
    if((Sys.Date() == "2018-12-31")){
        return("Year Day")
    }
    
    # I'm adding one because first days of months in the IFC are tied to fixed dates in the GC:
    # https://en.wikipedia.org/wiki/International_Fixed_Calendar
    d = 1 + ddelta
    
    #If short then return in ISO 86011 format, if not then return the date as...words?
    if(short == 0){
        
        return(paste(m_name, paste(d, ",", sep = ""), y, sep = " "))
        
    }else{
        #Padding the day's numerical representation with 0 if necessary
        d2 <- ifelse(nchar(d) < 2, paste("0", d, sep = ""), d)
        return(paste(y, m_id, d2, sep = "-"))
    }
}

# Viz

# https://dominikkoch.github.io/Calendar-Heatmap/

# source("./workspace/current/helper_func.R")
# 
# stock <- "MSFT"
# start.date <- "2014-00-01" # workaround for a small bug with the month extraction
# end.date <- Sys.Date()
# quote <- paste("http://ichart.finance.yahoo.com/table.csv?s=",
#                stock,
#                "&a=", substr(start.date,6,7),
#                "&b=", substr(start.date, 9, 10),
#                "&c=", substr(start.date, 1,4), 
#                "&d=", substr(end.date,6,7),
#                "&e=", substr(end.date, 9, 10),
#                "&f=", substr(end.date, 1,4),
#                "&g=d&ignore=.csv", sep="")             
# stock.data <- read.csv(quote, as.is=TRUE)
# 
# require(lubridate)
# 
# dates <- ymd(stock.data$Date)
# values <- stock.data$Adj.Close
# 
# calendarHeatmap(dates, values,
#                 title = "Microsoft Stock Price",
#                 subtitle = "Yahoo Finance API", legendtitle = "Price")