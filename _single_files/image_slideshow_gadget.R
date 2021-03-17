library(shiny)
library(slickR)
library(miniUI)

image_slideshow <- function(path) {

  ui <- miniPage(
    gadgetTitleBar("My Gadget"),
    miniContentPanel(
      slickROutput("slickr", width = "1500px")
    )
  )

  server <- function(input, output, session) {
    output$slickr <- renderSlickR({
      imgs <- list.files(path, pattern = ".jpg", full.names = TRUE)
      slickR(imgs)
    })
  }

  runGadget(ui, server)
}

image_slideshow("/home/gordon/workspace/current/vader/a_general/process_runs/1_processing/run_11_ex")

