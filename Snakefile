import os

slides = config["slides"]

rule all_formats:
    input:
        expand(
            "slides-1080p60.{ext}",
            ext=["html", "pdf", "pptx"]
        )


rule slides:
    input:
        expand(
            os.path.join('media/videos/{slide}/{{res}}/{slide}.mp4'),
            slide=slides
        )
    output:
        'slides-{res}.{ext}'
    shell:
        'manim-slides convert --to {wildcards.ext} {slides} {output}'

rule present:
    input:
        expand(
            os.path.join('media/videos/{slide}/1080p60/{slide}.mp4'),
            slide=slides
        )
    shell:
        'manim-slides present  {slides} {output}'


rule qh:
    input:
        os.path.join('{slide}.py')
    output:
        os.path.join('media/videos/{slide}/1080p60/{slide}.mp4')
    shell:
        'manim {wildcards.slide}.py {wildcards.slide} '


rule ql:
    input:
        os.path.join('{slide}.py')
    output:
        os.path.join('media/videos/{slide}/480p15/{slide}.mp4')
    shell:
        'manim -ql {wildcards.slide}.py {wildcards.slide}'


rule preview:
    input:
        expand(
            os.path.join('media/images/{slide}/{slide}.png'),
            slide=slides
        )
    output:
        os.path.join('preview.pdf')
    shell:
        # 'magick montage -mode concatenate {input} {output}'
        'convert {input} {output}' # && open {output}'

rule png_ql:
    input:
        os.path.join('{slide}.py')
    output:
        os.path.join('media/images/{slide}/{slide}.png')
    shell:
        'manim -qh -s --format=png -o {wildcards.slide}.png {input} {wildcards.slide}'
