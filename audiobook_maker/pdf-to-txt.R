library(pdftools)
library(argparser)

p <- arg_parser("Extract text from pdf")
p <- add_argument(p, "--file", help = "Path to pdf")
argv <- parse_args(p)

output_file_name <-  gsub("pdf", "txt", argv$file)
output_file_name <- gsub("raw", "txt", output_file_name)
text <- pdf_text(argv$file)
te = paste(text, collapse = " ")
fileConn <- file(output_file_name)
writeLines(te, fileConn)
close(fileConn)

print(output_file_name)
