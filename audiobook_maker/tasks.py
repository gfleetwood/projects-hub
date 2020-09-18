from invoke import task

@task
def txt_build(c, file):
    c.run("Rscript pdf-to-txt.R --file {}".format(file))
    
@task
def mp3_build(c, file):
    c.run(
    "python txt-to-mp3.py \
    --txt_from_web=0 \
    --source={}".format(file)
    )
