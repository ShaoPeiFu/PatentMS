import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sinaPatent.settings")

import django

django.setup()
from PatentMS.models import Category, Page


def populate():

    python_pages = [
        {
            "title": "Official Python Tutorial",
            "url": "http://docs.python.org/2/tutorial/",
        },
        {
            "title": "How to Think like a Computer Scientist",
            "url": "http://www.greenteapress.com/thinkpython/",
        },
        {
            "title": "Learn Python in 10 Minutes",
            "url": "http://www.korokithakis.net/tutorials/python/",
        },
    ]

    django_pages = [
        {
            "title": "Official Django Tutorial",
            "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
        },
        {"title": "Django Rocks", "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django", "url": "http://www.tangowithdjango.com/"},
    ]

    other_pages = [
        {"title": "Bottle", "url": "http://bottlepy.org/docs/dev/"},
        {"title": "Flask", "url": "http://flask.pocoo.org"},
    ]

    # 新增的分类（不包含页面）
    pascal_pages = []
    perl_pages = []
    php_pages = []
    prolog_pages = []
    postscript_pages = []
    programming_pages = []

    cats = {
        "Python": {"pages": python_pages},
        "Django": {"pages": django_pages},
        "Other Frameworks": {"pages": other_pages},
        "Pascal": {"pages": pascal_pages},
        "Perl": {"pages": perl_pages},
        "PHP": {"pages": php_pages},
        "Prolog": {"pages": prolog_pages},
        "PostScript": {"pages": postscript_pages},
        "Programming": {"pages": programming_pages},
    }

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])
            for p in Page.objects.filter(category=c):
                print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


if __name__ == "__main__":
    print("Starting population script...")
    populate()
    print("Population script finished.")
