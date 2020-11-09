library(shiny)
library(tidyverse)
library(odbc)
library(DBI)
library(purrr)
library(DT)
library(glue)

server <- function(input, output, session) {
  
  values <- reactiveValues()
  
  observeEvent(
    input$con, 
    {
      values$db_con <- dbConnect(
        odbc::odbc(),
        Driver = Sys.getenv("DRIVER"), 
        Database = Sys.getenv("DATABASE"), 
        Port = Sys.getenv("PORT"), 
        Server = Sys.getenv("SERVER"), 
        UID = Sys.getenv("USERNAME"), 
        PWD = Sys.getenv("PASSWORD"),
        sslmode = "require"
      )
      values$connection_msg <- "Database Connection Established"
      
      insertUI(
        selector = '#placeholder',
        ui = selectInput("tbl", "Choose Table", dbListTables(values$db_con))
      )
      
    }
    )
  
  
  output$con_msg <- renderText({values$connection_msg})
  output$history <- renderDT(values$history)
  
  observeEvent(
    input$read,
    {
      values$tbl <- dbGetQuery(values$db_con, glue("SELECT * FROM {input$tbl}"))
      
      # values$history <- data.frame(
      #   row = integer(),
      #   col = integer(),
      #   original_value = character(), 
      #   updated_value = character(), 
      #   row_nums = integer(),
      #   stringsAsFactors = FALSE
      #   ) 
      
      values$history <- dbGetQuery(values$db_con, glue("SELECT * FROM {input$tbl}_change_log"))
      } 
  )
  
  output$table <- renderDT(values$tbl, editable = 'cell')
  
  observeEvent(
    input$table_cell_edit, 
    {
      
    info <- input$table_cell_edit
    original_val <- values$tbl[info$row, info$col]
    
    changes <- data.frame(
      row = info$row,
      col = info$col,
      original_value = original_val, 
      updated_value = info$value, 
      created = Sys.time() %>% as.POSIXlt("UTC", "%Y-%m-%dT%H:%M:%S") %>% strftime("%Y-%m-%dT%H:%M:%S%z"),
      stringsAsFactors = FALSE
      ) 
    
    values$history <- changes %>% 
      mutate(row_nums = 0) %>% 
      rbind(values$history, .) %>%
      mutate(row_nums = seq(1, n(), 1))
    
    values$tbl <- editData(values$tbl, input$table_cell_edit, 'table')
    
  }
  )
  
  observeEvent(
    input$update,
    {
      dbWriteTable(values$db_con, input$tbl, values$tbl, overwrite = TRUE)
      dbWriteTable(values$db_con, glue("{input$tbl}_change_log"), values$history, append = TRUE)
    }
  )
  
}

sidebar <- sidebarPanel(
  actionButton("con", "Connect To Database"),
  tags$div(id = 'placeholder'),
  actionButton("read", "Read From Database"),
  actionButton("update", "Update Database")
)

main_area <- mainPanel(
  h3("Data"),
  textOutput("con_msg"),
  DTOutput("table"),
  h3("Change History"),
  DTOutput("history")
  )

layout <- sidebarLayout(sidebar, main_area)
title <- titlePanel("DB RU App")
ui <- fluidPage(title, layout)
app <- shinyApp(ui = ui, server = server)
