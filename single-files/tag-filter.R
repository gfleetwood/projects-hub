library(shiny)
library(tagsinput)
library(DT)

tags_to_list <- function(x){
    
    result <- map(x, ~ as.vector(unlist(str_split(.x, ",")))) %>% 
        flatten_chr() %>% 
        map_chr(~ str_trim(.x))
    
    return(result)
}

check_intersect <- function(x, y){
    
    result <- length(intersect(tags_to_list(x), y))
    
    return(result)
}

#item, tags, notes
# df = data.frame(item = c("test"), tags = c("test1, test 2, test3"),
#notes = c("This is  atest"))
df <- read_csv("~/../Desktop/other/tagger/test.csv")
tags_ref <- tags_to_list(df$tags)

ui <- fluidPage(

    # Application title
    titlePanel("Old Faithful Geyser Data"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            selectizeInput(
                'e2', 'Select', choices = tags_ref, multiple = TRUE),
            tagsTextInput("tags", "Tags", "placeholder"),
            textOutput("out")
        ),

        # Show a plot of the generated distribution
        mainPanel(
            DTOutput('tbl'),
            textOutput("e3")
        )
    )
)

server <- function(input, output) {
    
    output$e3 <- renderText({input$e2})
    output$out <- renderPrint(strsplit( input$tags, ",")[[1]])
    
    output$tbl = renderDT(
        {
            tags_input <- input$e2
            
            df_filtered <- df %>%
                mutate(tag_match = map_dbl(
                    tags, ~ check_intersect(.x, tags_input))) %>%
                filter(tag_match >  0) %>% 
                select(-tag_match)
            
            df_filtered
        }
                          , 
    options = list(lengthChange = FALSE)
    )
    
}

shinyApp(ui = ui, server = server)
