shinyUI(
  fluidPage(
    sidebarLayout(
      sidebarPanel(
        includeMarkdown("app_intro.md")
                  ), #end sidebarPanel
      mainPanel(
        br(),
        br(),
        textInput('generations', 
                  "NUMBER OF GENERATIONS", 
                  value = "10"),
        actionButton("seed", "SEED"),
        actionButton("run", "RUN"),
        br(),
        h4('Target:'),
        textOutput("target"),
        h4('Numbers:'),
        textOutput("nums"),
        br(),
        h4('Algorithm\'s Best Solution:'),
        textOutput("exp"),
        h4('Evaluation:'),
        textOutput("ans"),
        h4('Fitness:'),
        textOutput("fitness"),
        h4('Time Taken:'),
        textOutput("time",inline = T)
                ) #end mainPanel
                ) #end sidebarLayout
  ) # end fluidPage
)#shinyUI