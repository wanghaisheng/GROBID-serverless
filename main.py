from platform import uname_result
from fastapi import FastAPI
import requests
import pandas as pd
from fastapi.responses import ORJSONResponse
import uvicorn
import scipdf

from pywebio.input import *
import os
from pywebio.io_ctrl import Output, OutputList
from pywebio.output import *
from pywebio.platform import seo
from pywebio.platform.page import config
from pywebio.session import run_js, set_env
from pywebio import config, session

from pywebio.platform.fastapi import asgi_app
import time
import pywebio_battery as battery
from app.constants import *
from supabase import create_client, Client
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote_plus, urlunparse

# 加载文件
load_dotenv(".env")
supabase_url = os.environ.get('supabase_url')
# supabase_url = 'https://bwrzzupfhzjzvuglmpwx.supabase.co'

print(supabase_url)
supabase_apikey = os.environ.get('supabase_apikey')
print(supabase_apikey)
supabase_db: Client = create_client(supabase_url, supabase_apikey)

app = FastAPI()

def strip_url_to_homepage(url: str) -> str:
    """
    Strip URL to its homepage.
    :param url: URL to strip, e.g. "http://www.example.com/page.html".
    :return: Stripped homepage URL, e.g. "http://www.example.com/"
    """
    # if not url:
    #     raise StripURLToHomepageException("URL is empty.")

    try:
        uri = urlparse(url)
        assert uri.scheme, "Scheme must be set."
        assert uri.scheme.lower() in ['http', 'https'], "Scheme must be http:// or https://"
        uri = (
            uri.scheme,
            uri.netloc,
            '/',  # path
            '',  # params
            '',  # query
            '',  # fragment
        )
        url = urlunparse(uri)
    except Exception as ex:
        print("Unable to parse URL {}: {}".format(url, ex))

    return url


def supabaseupdate(tablename, user, domain):
    try:
        data = supabase_db.table(tablename).update(
            user).eq("domain", domain).execute()
    except:
        raise Exception


def supabaseop(tablename, users):
    try:
        data = supabase_db.table(tablename).insert(users).execute()
    except:
        raise Exception


def trueurl(url):

    r = requests.head(url, allow_redirects=True)
    return r.url


def formatdomain(url):

    if url.startswith("http://"):
        domain = urlparse(url).netloc
    elif url.startswith("https://"):
        domain = urlparse(url).netloc

    else:
        domain = url.split('/')[0]
    print('domain is ', domain)
    if not 'www' in domain:
        domain = 'www.'+domain
    return domain


@app.get("/pdf2dict/", response_class=ORJSONResponse)
def pdf2dict(url: str):
    # print('check url', url)
    results = []
    # test='https://www.biorxiv.org/content/biorxiv/early/2018/11/20/463760.full.pdf'
    try:
        article_dict = scipdf.parse_pdf_to_dict(url, as_list=False)
    except:
        print('there is error')
    return {"results": article_dict}

return_home = """
location.href='/'
"""


def check_form(data):
    # if len(data['name']) > 6:
    #     return ('name', 'Name to long!')
    # if data['age'] <= 0:
    #     return ('age', 'Age cannot be negative!')
    pass


def does_url_exist(url):
    try: 
        r = requests.head(url)
        if r.status_code < 400:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(e)
        # handle your exception


@config(theme="minty", title=SEO_TITLE, description=SEO_DESCRIPTION)
def index() -> None:
    # Page heading
    put_html(LANDING_PAGE_HEADING)
    lang = 'English'
    if lang == 'English':
        LANDING_PAGE_DESCRIPTION = LANDING_PAGE_DESCRIPTION_English
    session.run_js(
        'WebIO._state.CurrentSession.on_session_close(()=>{setTimeout(()=>location.reload(), 40000})')

    with use_scope('introduction'):
        # put_html(PRODUCT_HUNT_FEATURED_BANNER)
        # put_html(LANDING_PAGE_SUBHEADING)
        put_markdown(LANDING_PAGE_DESCRIPTION, lstrip=True)
    # run_js(HEADER)
    # run_js(FOOTER)

    inputdata = input_group("scipdf based on grobid", [
        input("input your pdf url",
             name='url'),
        radio("pls choose?", [
              'urlpdf', 'localpdf','figures'], inline=True, name='q1')

    ], validate=check_form)

    url = inputdata['url']
    print('check url', url)

    q1 = inputdata['q1']
    # if not isvaliddomain(url):
    #     return {"urls": 'not a valid domain'}
    if url.startswith("http://"):
        pass
    elif url.startswith("https://"):
        pass
    else:
        url = 'https://'+url
    # url =trueurl(url)

    with use_scope('loading'):

        put_loading(shape='border', color='success').style(
            'width:4rem; height:4rem')
    clear('introduction')

    put_html('</br>')
    set_env(auto_scroll_bottom=True)
    urls = []
    # with use_scope('log'):

    #     with battery.redirect_stdout():

    #         urls = crawler(url, 1)
    data = []
    article_dict=''
    if q1 == 'urlpdf':
        # with use_scope('log'):

        #     with battery.redirect_stdout():

        #         domain = url
        #         # data = supabase_db.table("shops").select(
        #             # 'subdomains').eq("domain", domain).execute()
        #         # print(type(data))
        #         # print('existing db',len(supabase_db.table("tiktoka_douyin_users").select('uid').execute()[0]),data,data[0])
        #         if len(data.data) > 0:
        #             print('this user exist', domain, data.data)
        #             urls = data.data
        #         else:
        #             put_text(
        #                 'first crawl for this domain ,it will takes some time')

        #             article_dict = scipdf.parse_pdf_to_dict(url, as_list=False)


        #             # supabaseupdate('shop', {'subdomains': urls}, domain)
        # clear('log')
        article_dict = scipdf.parse_pdf_to_dict(url, as_list=False)

        if article_dict=='':
            put_text('there is no result extract in this paper', url)
            put_button("Try again", onclick=lambda: run_js(
                return_home), color='success', outline=True)

    elif q1=='figures':
        start = time.time()
        domain = trueurl(domain)

        end = time.time()
        put_text('Parsing is complete! time consuming: %.4fs' %
                    (end - start))

    elif q1=='localpdf':
        start = time.time()


        end = time.time()
        put_text('Parsing is complete! time consuming: %.4fs' %
                    (end - start))

    # put_logbox('log',200)
    if not article_dict=='':

        array=article_dict.encode('utf-8')
        clear('loading')
        clear('log')

        put_collapse('parsing result', put_table(
            [article_dict['title'],article_dict['abstract'],article_dict['doi']], header=['title', 'abstract', 'doi']))

        put_collapse('sections', put_table(
            article_dict['sections'], header=['heading', 'text']))
        put_collapse('references', put_table(
            article_dict['references'], header=['title', 'year', 'journal','author']))
        put_collapse('figures', put_table(
            article_dict['figures'], header=['figure_label', 'figure_type', 'figure_caption']))
        put_row([
            put_button("Try again", onclick=lambda: run_js(
                return_home), color='success', outline=True),
            put_button("Back to Top", onclick=lambda: run_js(
                scroll_to('ROOT', position='top')), color='success', outline=True),
            put_file(urlparse(url).netloc+'.txt',
                     array, 'download all')
        ])


home = asgi_app(index)

app.mount("/", home)


# api.mount('/static', StaticFiles(directory='static'), name='static')
# api.include_router(home.router)
# api.include_router(weather_api.router)


if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    if (os.environ.get('PORT')):
        port = int(os.environ.get('PORT'))
    else:
        port = 5001

    uvicorn.run(app='main:app',
                host="0.0.0.0",
                port=port,
                reload=False,
                debug=True,
                proxy_headers=True,
                log_config=log_config)
