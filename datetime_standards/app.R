library(tidyverse)
library(shiny)
library(calheatmapR)
source("ifc.R")

df <- read_csv("international_fixed_calendar.csv") 
# yr <- Sys.Date() %>% lubridate::year()
# mnth <- Sys.Date() %>% lubridate::month()
# dy <- Sys.Date() %>% lubridate::day()
# curr_md = paste(mnth, dy, sep = '-')

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   titlePanel("New Datetime Standards"),
   h3(textOutput("cap")),
   #h3(textOutput("time")),
   includeMarkdown("text.md")
)

# Define server logic required to draw a histogram
server <- function(input, output, session) {
    
    
    output$cap <- renderText({
       
       invalidateLater(1000, session)
       
       #Cast time to UTC
       dt <- lubridate::with_tz(Sys.time(), tzone = 'UTC') %>% as.character()
       yr <- Sys.Date() %>% lubridate::year()
       mnth <-Sys.Date() %>% lubridate::month()
       dy <- Sys.Date() %>% lubridate::day()
       curr_md = paste(mnth, dy, sep = '-')

       ifc <- df %>%
           filter( (curr_md > start) & (curr_md < end) ) %>%
           mutate(
               days_delta = reconstruct_date(yr, start),
               ifc_date_short = ifc_date(yr, month_id, month, days_delta),
               ifc_date_long = ifc_date(yr, month_id, month, days_delta, short = 0)
           ) %>% pull(ifc_date_short)

       return(paste(ifc, str_split(dt, " ")[[1]][2], sep = " "))
       
   })
    
    output$time <- renderText({
        
        invalidateLater(1000, session)
        return(paste("Time: ", str_split(dt, " ")[[1]][2], sep = " "))
        
    })
}

shinyApp(ui = ui, server = server)

