# setup

library(googledrive)
library(glue)
library(purrrlyr)
library(readr)
library(purrr)
library(magrittr)

drive_auth(path = "~/misc/goog-oauth.json")

blog_loc = "/home/paperspace/projects/gdocs-cms"
static_loc = glue("{blog_loc}/static/post")
gdoc_loc = glue("{blog_loc}/gdocs")

setwd(blog_loc)

# Clear out blog posts & media
system(glue("rm -rf {blog_loc}/content/post/*"))
system(glue("rm -rf static_loc/*"))

blog_posts = drive_ls(as_id("1zvpbczKjZL0q6W-O54vtPJx4NvsDPPI9"))

get_tags <- function(){
  
  # Tags are in this form in the doc: "tags: image test, dog"
  # We want them to in this form for the blog: "'image test','dog'"
  
  result <- read_file(glue("{gdoc_loc}/tags.txt")) %>% 
    trimws() %>% 
    strsplit(": ") %>%
    unlist() %>% 
    extract2(2) %>%
    strsplit(", ") %>% 
    map(~ paste("'", .x, "'", sep = "")) %>%
    unlist() %>% 
    paste(collapse = ",")
  
  return(result)
  
}

process_blog_post <- function(blog_post){
  
  # download the file
  drive_download(
    file = as_id(blog_post$id),
    path = glue("{gdoc_loc}/{blog_post$name}"),
    overwrite = T)

  # Convert doc to zip, make folder to store extraction, and extract
  system(glue("cp {gdoc_loc}/{blog_post$name}.docx {gdoc_loc}/{blog_post$name}.zip"))
  system(glue("unzip {gdoc_loc}/{blog_post$name}.zip -d {gdoc_loc}/{blog_post$name}"))

  # Copy media files from extraction to blog static folder for doc
  system(glue("mkdir -p {static_loc}/{blog_post$name}"))
  system(glue("cp {gdoc_loc}/{blog_post$name}/word/media/* {static_loc}/{blog_post$name}"))

  # Convert doc to markdown
  system(glue("pandoc -s {gdoc_loc}/{blog_post$name}.docx -t markdown -o {gdoc_loc}/{blog_post$name}.md"))

  # replace media in md with link to static folder
  system(glue("sed -i 's.media./post/{blog_post$name}.g' {gdoc_loc}/{blog_post$name}.md"))

  # Save tags
  system(glue('grep "tags" {gdoc_loc}/{blog_post$name}.md > {gdoc_loc}/tags.txt'))

  # Remove tags from doc
  system(glue('grep -v "tags" {gdoc_loc}/{blog_post$name}.md > {gdoc_loc}/temp2.md'))
  system(glue("cp {gdoc_loc}/temp2.md {gdoc_loc}/{blog_post$name}.md"))

  # Remove possible image specs which don't work for some reason.
  #system(glue("sed -i 's/{.*}//g' {gdoc_loc}/{blog_post$name}.md"))
  
  # add yaml to md
  
  title = blog_post$drive_resource[[1]]$name
  date = blog_post$drive_resource[[1]]$createdTime
  tags = get_tags()
  draft = "false"
  author = blog_post$drive_resource[[1]]$owners[[1]]$displayName
  
  file_to_write <- c(
    "+++",
    glue('title = "{title}"'),
    glue('date = "{date}"'),
    glue('tags = [{tags}]'),
    glue('draft = "{draft}"'),
    glue('author = "{author}"'),
    "+++"
  )
  
  fileConn <- file(glue("{gdoc_loc}/yaml-header.txt"))
  writeLines(file_to_write, fileConn)
  close(fileConn)
  
  system(glue("cat {gdoc_loc}/yaml-header.txt {gdoc_loc}/{blog_post$name}.md >> {gdoc_loc}/temp.md"))
  system(glue("cp {gdoc_loc}/temp.md {gdoc_loc}/test.md -f"))
  
  # put md in content folder: overwriblog_posts file with same name
  system(glue("mv {gdoc_loc}/{blog_post$name}.md {blog_loc}/content/post -f"))
  
  # clean gdocs folder
  system(glue("rm -rf {gdoc_loc}/*"))
  
  # build site
  blogdown::build_dir(blog_loc)
  
  # git push
  system(glue("git add . && git commit -m 'Add blog {blog_post$name}' && git push origin master"))
  
}

by_row(blog_posts, ~ process_blog_post(.x), .collate = "col")
