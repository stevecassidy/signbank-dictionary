
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

from tagging.models import Tag, TaggedItem
from .models import Gloss


def taglist_json(request):
    """Return a list of tags as JSON"""

    tags = [t.name for t in Tag.objects.all()]

    return HttpResponse(json.dumps(tags), {'content-type': 'application/json'})



def taglist(request, tag=None):
    """View of a list of tags or a list of signs with a given tag"""


    if tag:
        # get the glosses with this tag
        tagobj = get_object_or_404(Tag, name=tag)
        gloss_list = TaggedItem.objects.get_by_model(Gloss, tagobj)

        if ':' in tag:
            taginfo = tag.split(':')
        else:
            taginfo = ('None', tag)


        paginator = Paginator(gloss_list, 50)

        if 'page' in request.GET:

            page = request.GET['page']
            try:
                result_page = paginator.page(page)
            except PageNotAnInteger:
                result_page = paginator.page(1)
            except EmptyPage:
                result_page = paginator.page(paginator.num_pages)

        else:
            result_page = paginator.page(1)



        return render(request, 'dictionary/gloss_list.html',
                      {'paginator': paginator,
                       'page': result_page,
                       'thistag': taginfo,
                       'tagdict': tag_dict()})
    else:
        return render(request, 'dictionary/gloss_list.html',
                      {'tagdict': tag_dict()})


def tag_dict():
    """Generate a dictionary of tags categorised by their
    category (the part before the colon)
    Returns a dictionary with categories as keys and
    each value being a list of tuples (tagname, count, fulltagname)"""

    tags = Tag.objects.usage_for_model(Gloss, counts=True)
    # build a dictionary of tags under their categories
    cats = dict()
    for tag in tags:
        if tag.name.find(':') >= 0:
            (cat, tagname) = tag.name.split(":", 1)
        else:
            cat = "None"
            tagname = tag.name

        if cat in cats:
            cats[cat].append((tagname, tag.count, tag.name))
        else:
            cats[cat] = [(tagname, tag.count, tag.name)]

    return cats
