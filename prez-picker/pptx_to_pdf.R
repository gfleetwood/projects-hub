library(pdftools)
library(glue)
library(stringr)
library(png)

office_shot <- function(file){
  cmd_ <- sprintf(
    "C:/Program Files/LibreOffice --headless --convert-to pdf --outdir %s",
    file)
  
  system(cmd_)
  
  pdf_file <- gsub("\\.(docx|pptx)$", ".pdf", basename("test.pdf"))
  pdf_file <- file.path(pdf_file)
  screen_imgs <- pdf_convert(pdf = pdf_file, format = "png", verbose = FALSE)
  unlink(pdf_file)
  screen_imgs
}

#office_shot(file = "C:/Users/Gordon/Desktop/me/presentation-picker/slides/input/test.pptx")

file = "C:\\Users\\Gordon\\Desktop\\me\\presentation-picker\\slides\\input"
f = glue("{file}\\test.pptx")
cmd_ <- glue(
'"C:\\Program Files\\LibreOffice\\program\\soffice.exe" --headless --convert-to pdf --outdir "{file}" "{f}"'
)

system("cmd.exe", input = cmd_)

pdf_file <- gsub("(docx|pptx)$", "pdf", f)
bitmap <- pdf_render_page(pdf_file, page = 1)
writePNG(bitmap, "~/../Desktop/page.png")
