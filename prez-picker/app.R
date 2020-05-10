library(shiny)
library(officer)
library(glue)
library(readr)
library(shinyFiles)
library(fs)
library(DT)
library(purrr)
library(stringr)
library(pdftools)
library(png)

base <- "C:/Users/Gordon/Desktop/me/presentation-picker/slides/intermediate"

ui <- fluidPage(

    titlePanel("Presentation Picker"),
 
    sidebarLayout(
        
        sidebarPanel(
            shinyFilesButton(
                'file', 
                label='File select', 
                title='Please select a file', 
                multiple = FALSE)),

        mainPanel(
            DTOutput('tbl'))
        
    )
)

server <- function(input, output, session) {
    
    volumes <- c(
        Home = path_home(),
        "R Installation" = R.home(),
        getVolumes()())
    
    shinyFileChoose(
        input, "file", roots = volumes, session = session, 
        filetypes = c('pptx'))
    
    output$tbl = renderDT({
        
        if(is.list(input$file)){
            
            df <- parseFilePaths(volumes, input$file)
            main(df$datapath)
            df
            
        } else{
            cat("No file selected yet")
        }
 
    })
    
    save_slide <- function(slide, slides, file, name, dir){
        
        to_remove = discard(slides, ~ .x == slide)
        
        temp = read_pptx(file)
        temp <- move_slide(temp, index = slide, to = 1)
        garbage = map(to_remove, ~ remove_slide(temp, 2))
        
        fpath = glue("{dir}/slide_{slide}.pptx")
        print(temp, target = fpath)
        
    }
    
    get_name <- function(fname){
        
        name <- fname %>% 
            str_split(., "/") %>% 
            unlist() %>% 
            tail(1) %>% 
            str_split("\\.") %>% 
            unlist() %>% 
            head(1)
        
        return(name)
        
    }
    
    slides_to_imgs <- function(dir){
        
        files <- list.files(path = dir, full.names = TRUE)
        temp <- map(files, ~ slide_to_img(dir, .x))
        
    }
    
    slide_to_img <- function(dir, file){
        
        cmd_ <- glue(
            '"C:\\Program Files\\LibreOffice\\program\\soffice.exe" --headless --convert-to pdf --outdir "{dir}" "{file}"'
        )
        
        
        system("cmd.exe", input = cmd_)
        Sys.sleep(5) # Time for the pdf to be created
        
        pdf_file <- gsub("(docx|pptx)$", "pdf", file)
        png_file <- gsub("(docx|pptx)$", "png", file)
        bitmap <- pdf_render_page(pdf_file, page = 1)
        writePNG(bitmap, png_file)
        unlink(pdf_file)
        
    }
    
    main <- function(ppt_name){
        
        
        # Get name of file & create directory
        name <- get_name(ppt_name)
        cat(name)
        dir <- file.path(base, name)
        dir.create(dir, showWarnings = FALSE)
        
        
        # Get number of slides
        pp = read_pptx(ppt_name)
        slide_nums = seq(1, length(pp), 1)

        # Split slides into one slide increments
        temp = map_chr(
            slide_nums,
            ~ save_slide(.x, slide_nums, ppt_name, name, dir))

        # Convert slides to images
        temp2 = slides_to_imgs(dir)
        
        
    }
    
}


shinyApp(ui = ui, server = server)
