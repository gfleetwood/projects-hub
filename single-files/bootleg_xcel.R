library(DT)
library(tidyverse)
library(shiny)
library(miniUI)
library(shinyjs)
library(shinyFiles)
library(rhandsontable)

sheetR <- function(viewer = paneViewer()) {
  
  ui <- miniPage(
    
    miniTitleBar(
      "SheetR"
      ),
    
    miniContentPanel(
      shinyFilesButton("file", "Open File", "Please select a file", multiple = F),
      shinySaveButton("save", "Save File", "Save file as...", 
                      filetype = list(csv = "csv")),
      useShinyjs(),  # Set up shinyjs
      runcodeUI(code = "shinyjs::alert('Hello!')", type = "textarea"),
      DTOutput('tbl')
      )
  ) # end UI
  
  server <- function(input, output, session) {
    
    runcodeServer()
    
    volumes <- c(Home = fs::path_home(), "R Installation" = R.home(), getVolumes()())
    shinyFileChoose(input, "file", roots = volumes, session = session)
    shinyFileSave(input, "save", roots = volumes, session = session, 
                  restrictions = system.file(package = "base"))
    
    output$tbl = renderDT({
      inFile <- parseFilePaths(volumes, input$file)
      if(NROW(inFile)) {
        df <- read_csv(as.character(inFile$datapath))
        df2 <<- df
      }
      df
    },
    options = list(autoWidth = T, paging = F, lengthChange = F), 
    editable = T
    )
    
    observe({
      fileinfo <- parseSavePath(volumes, input$save)
      print(fileinfo)
      print(as.character(fileinfo$datapath))
      if (nrow(fileinfo) > 0) {
        write_csv(df2, as.character(fileinfo$datapath))
      }
    })
    
    observe({
      print(input$tableID_cell_edit)
      df2[i, j] <<- input$tableID_cell_edit
      })
    
  }
  
  runGadget(ui, server)
}

sheetR()