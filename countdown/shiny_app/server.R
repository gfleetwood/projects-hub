shinyServer(function(input, output) {
  
  values <- reactiveValues(
    ga.results =  NULL,
    target.nums.ops = NULL,
    fitness.value = NULL
  )
  
  observeEvent(input$seed, {
    values$target.nums.ops <- setup()
  })

  observeEvent(input$run, {
    withProgress(message = 'Running Algorithm', value = 0, 
                 {
    values$ga.results <- run.countdown(values$target.nums.ops[['nums']],
                                       values$target.nums.ops[['ops']],
                                       values$target.nums.ops[['target']],
                                       as.integer(input$generations))
                  })
    values$fitness.value <- fitness.indiv(values$ga.results[[2]],
                                          values$target.nums.ops[['target']])
    
  })
  
  output$target <- renderPrint({ 
    #values$target.nums.ops[['target']]
    ifelse(is.null(values$target.nums.ops[['target']]),
           '',
           values$target.nums.ops[['target']])
  })
  
  output$nums <- renderPrint({ 
    paste0(as.character(values$target.nums.ops[['nums']]),
           collapse = ', ')
  })
  
  output$exp <- renderText({
    paste0(values$ga.results[[2]], collapse = '')
    })
  
  output$ans <- renderText({
    as.character(result(values$ga.results[[2]]))
  })
  
  output$fitness <- renderText({
    values$fitness.value
  })
  
  output$time <- renderText({
    ifelse(is.null(values$ga.results[[3]]),
           c('0 seconds'),
           paste(round(values$ga.results[[3]],2), attr(values$ga.results[[3]], 'units')))
  })
  
}) #End shinyServer