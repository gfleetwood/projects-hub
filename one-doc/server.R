

# Define server logic required to draw a histogram
shinyServer(function(input, output, session) {
    
    output$hot = renderRHandsontable({
        if (!is.null(input$hot)) {
            DF = hot_to_r(input$hot)
        } else {
            DF = read.csv("test.csv", stringsAsFactors = FALSE)
            DF = df
        }
        
        #df <<- DF
        
        rhandsontable(DF[1:10]) %>%
            hot_table(highlightCol = TRUE, highlightRow = TRUE)
    })
    
    output$knitDoc <- renderUI({
        input$eval
        return(isolate(HTML(knit2html(text = input$rmd, fragment.only = TRUE, quiet = TRUE))))
    }) 
    
    output$knitDoc2 <- renderUI({
        input$eval2
        return(isolate(HTML(knit2html(text = input$rmd2, fragment.only = TRUE, quiet = TRUE))))
    })
    
})
