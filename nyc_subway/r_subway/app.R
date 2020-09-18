library(shiny)
library(DT)
library(dplyr)

df <- read.csv("https://gist.githubusercontent.com/gfleetwood/c35710d4466c40de3c95bdb411d16a31/raw/c682f96fa81dfe2ee68962c394712210bca6aa57/nyc-subway.csv")
trains <- setNames(
  as.character(unique(df$Train)),
  as.character(unique(df$Train))
  )

stations <- setNames(
  as.character(unique(df$Stations)),
  as.character(unique(df$Stations))
)

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("NYC Metro"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
        selectInput('train', "Trains", trains, selected = trains[1])
      ),
      # Show a plot of the generated distribution
      mainPanel(
        DTOutput("tbl")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  output$tbl <- renderDT(df %>% filter(Train == input$train))
}

# Run the application 
shinyApp(ui = ui, server = server)

