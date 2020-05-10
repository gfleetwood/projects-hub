# An attempt to build an ssh & scp app.

library(shiny)
library(ssh)
library(tidyverse)
library(glue)

#https://github.com/ficonsulting/RInno
#https://cran.r-project.org/web/packages/ssh/vignettes/intro.html
#https://github.com/colearendt/shiny-shell

# Define UI for application that draws a histogram
ui <- fluidPage(
  
  titlePanel("SSH SCP"),
  
  sidebarLayout(
    sidebarPanel(
      textInput("server", "Enter Server", value = "", width = NULL, placeholder = NULL),
      textInput("pwd", "Enter Password", value = "", width = NULL, placeholder = NULL),
      actionButton('cxn', label='Connect'),
      fileInput("file", "Choose CSV File", 
                accept = c("text/csv", 
                           "text/comma-separated-values,text/plain",
                           ".csv")
                ),
      actionButton('up', label='Upload')
            ),
   mainPanel(
      "SSH SCP",
      textInput('command', 'Enter Command', value = "pwd"),
      actionButton('execute', label = 'Run'),
      verbatimTextOutput("text"),
      verbatimTextOutput("text2")
    )
  )
)

# Define server logic required to draw a histogram
server <- function(input, output, session) {
  
  values <- reactiveValues(session=0)
  
  eventReactive(
    input$cxn, {
        values$session <- ssh_connect(input$server, passwd = input$pwd)
      }
  )
  
  # eventReactive(input$cxn, {
  #   updateTextInput(session, "server", label = "Enter Server", value = "root@167.99.149.235")
  #   updateTextInput(session, "pwd", label = "Enter Password", value = "genspaceiot")
  # })
  
  output$text <- eventReactive(
    input$execute, {
        sess <- values$session
        print(sess)
        returnval <- capture.output(ssh_exec_wait(sess, command = input$command))[1]
        return(paste(returnval, collapse = '\n'))
    }
  )
  
  output$text2 <- eventReactive( 
    input$up, {
      inFile <- input$file
      if (is.null(inFile)) return(NULL)
      print(inFile)
      returnval <- capture.output(scp_upload(sess, inFile$datapath, to = "."))
      return(paste(returnval, collapse = '\n'))
    }
  )
  
  # Not working but the goal is to exit the session when the app is closed 
  
  # cancel.onSessionEnded <- session$onSessionEnded(function() {
  #   print("Disconnecting")
  #   ssh_disconnect(values$session)
  # })
  
  # on.exit(cancel.onSessionEnded())
  
}                 

# Run the application 
shinyApp(ui = ui, server = server)

