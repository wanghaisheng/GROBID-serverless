# Deploy fastAPI to Heroku using Docker

[FastAPI](https://fastapi.tiangolo.com/) Modern, fast, web framework for Python  
[Docker](https://www.docker.com/) Containerization software  
[Heroku](https://www.heroku.com/) Hosting platform

## Requirements

[Git](https://git-scm.com/) (or just download the repo)  
[Heroku cli](https://devcenter.heroku.com/articles/heroku-cli) (to run the heroku commands)


## db backend

https://github.com/vicogarcia16/fastapi_airtable


## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wanghaisheng/GROBID-serverless)

## Instructions


>https://link-discovery.herokuapp.com/sitemap/?url=


https://link-discovery.herokuapp.com/sitemap/?url=https://x.hacking8.com/



```python
import scipdf
article_dict = scipdf.parse_pdf_to_dict('example_data/futoma2017improved.pdf') # return dictionary
 
# option to parse directly from URL to PDF, if as_list is set to True, output 'text' of parsed section will be in a list of paragraphs instead
article_dict = scipdf.parse_pdf_to_dict('https://www.biorxiv.org/content/biorxiv/early/2018/11/20/463760.full.pdf', as_list=False)

# output example
>> {
    'title': 'Proceedings of Machine Learning for Healthcare',
    'abstract': '...',
    'sections': [
        {'heading': '...', 'text': '...'},
        {'heading': '...', 'text': '...'},
        ...
    ],
    'references': [
        {'title': '...', 'year': '...', 'journal': '...', 'author': '...'},
        ...
    ],
    'figures': [
        {'figure_label': '...', 'figure_type': '...', 'figure_id': '...', 'figure_caption': '...', 'figure_data': '...'},
        ...
    ],
    'doi': '...'
}

xml = scipdf.parse_pdf('example_data/futoma2017improved.pdf', soup=True) # option to parse full XML from GROBID
```

To parse figures from PDF using [pdffigures2](https://github.com/allenai/pdffigures2), you can run

```python
scipdf.parse_figures('example_data', output_folder='figures') # folder should contain only PDF files
```

You can see example output figures in `figures` folder.
