from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tagging.models import Tag, TaggedItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe

#from django.utils.encoding import smart_unicode

import os

from .models import *
from .forms import *
#from signbank.feedback.models import *
#from signbank.pages.models import *

from video.forms import VideoUploadForm


def dictionary_context_processor(request):
    """Context Processor to inject search form into every page
    on the site."""

    return {'menusearchform': UserSignSearchForm(auto_id="id_menu_%s"),
            'regionform': SetRegionForm(),
            }


def login_required_config(function):
    '''
    Like @login_required if the ALWAYS_REQUIRE_LOGIN setting is True.
    '''
    def wrapper(*args, **kwargs):
        if getattr(settings, 'ALWAYS_REQUIRE_LOGIN', False):
            decorated_function = login_required(function)
            return decorated_function(*args, **kwargs)
        else:
            return function(*args, **kwargs)
    return wrapper

def map_image_for_regions(regions):
    """Get the right map images for this region set
    """

    # Add a map for every unique language and dialect we have
    # regional information on
    # This may look odd if there is more than one language
    images = []
    for region in regions.all():
        language_name = region.dialect.language.name.replace(" ", "")
        dialect_name = region.dialect.name.replace(" ", "")
        dialect_extension = ""
        if region.traditional:
            dialect_extension = "-traditional"

        language_filename = "img/maps/" + language_name + ".png"
        dialect_filename = "img/maps/" + language_name + "/" + dialect_name + dialect_extension + ".png"

        if language_filename not in images:
            images.append(language_filename)
        if dialect_filename not in images:
            images.append(dialect_filename)

    return images

def variant(request, idgloss):

    if 'feedbackmessage' in request.GET:
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False

    gloss = Gloss.objects.filter(idgloss=idgloss)[0]

    # and all the keywords associated with this sign
    allkwds = gloss.translation_set.all()

    homophones = gloss.relation_sources.filter(role=Relationrole.objects.get(role="homophone"))

    # work out the number of this gloss and the total number
    can_view_not_inWeb = request.user.has_perm('dictionary.search_gloss')

    (glossposn, glosscount) = get_gloss_position(gloss, can_view_not_inWeb)

    videourl = gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None

    # navigation gives us the next and previous signs
    nav = gloss.navigation(request.user.has_perm('dictionary.search_gloss'))

    # the gloss update form for staff

    if request.user.has_perm('dictionary.search_gloss'):
        update_form = GlossModelForm(instance=gloss)
        video_form = VideoUploadForm(initial={'category': 'Gloss',
                                              'tag': gloss.pk,
                                              'redirect': request.get_full_path()})
    else:
        update_form = None
        video_form = None

    # Regional list (sorted by dialect name) and regional template contents if this gloss has one
    regions = sorted(gloss.region_set.all(), key=lambda n: n.dialect.name)
    try:
        page = Page.objects.get(url__exact=gloss.regional_template)
        regional_template_content = mark_safe(page.content)
    except:
        regional_template_content = None

    return render(request, "dictionary/variant.html",
                              {'translation': None,
                               'viewname': 'words',
                               'definitions': gloss.definitions(),
                               'gloss': gloss,
                               'allkwds': allkwds,
                               'n': 0,
                               'total': 0,
                               'matches': list(range(1, 1)),
                               'navigation': nav,
                               'dialect_image': map_image_for_regions(gloss.region_set),
                               'regions': regions,
                               'regional_template_content': regional_template_content,
                               # lastmatch is a construction of the url for this word
                               # view that we use to pass to gloss pages
                               # could do with being a fn call to generate this name here and elsewhere
                               'lastmatch': None,
                               'videofile': videourl,
                               'update_form': update_form,
                               'videoform': video_form,
                               'gloss': gloss,
                               'glosscount': glosscount,
                               'glossposn': glossposn,
                               'feedback' : True,
                               'feedbackmessage': feedbackmessage,
                               'tagform': TagUpdateForm(),
                               'SIGN_NAVIGATION' : settings.SIGN_NAVIGATION,
                               'SETTINGS_SHOW_TRADITIONAL' : settings.SHOW_TRADITIONAL,
                               'SETTINGS_SHOW_FREQUENCY' : settings.SHOW_FREQUENCY,
                               'DEFINITION_FIELDS' : settings.DEFINITION_FIELDS,
                               })

def word(request, keyword, n):
    """View of a single keyword that may have more than one sign"""

    n = int(n)

    if 'feedbackmessage' in request.GET:
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False

    word = get_object_or_404(Keyword, text=keyword)

    # returns (matching translation, number of matches)
    (trans, total) =  word.match_request(request, n, )

    # and all the keywords associated with this sign
    allkwds = trans.gloss.translation_set.all()

    trans.homophones = trans.gloss.relation_sources.filter(role__role__exact="homophone")

    # work out the number of this gloss and the total number
    can_view_not_inWeb = request.user.has_perm('dictionary.search_gloss')
    gloss = trans.gloss
    (glossposn, glosscount) = get_gloss_position(gloss, can_view_not_inWeb)

    videourl = trans.gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None

    thumbnails = None
    variant_relations = Relation.objects.filter(source__exact=gloss, role__role__exact="variant")

    if request.user.has_perm('dictionary.search_gloss'):
        variants = [relation.target for relation in variant_relations]
    else:
        variants = [relation.target for relation in variant_relations if relation.target.inWeb == True]

    if len(variants) > 0:
        thumbnails = []
        for variant in variants:
            thumbnail = {}
            thumbnail['pk'] = variant.pk
            thumbnail['idgloss'] = variant.idgloss
            thumbnails.append(thumbnail)

    # navigation gives us the next and previous signs
    nav = gloss.navigation(request.user.has_perm('dictionary.search_gloss'))

    # the gloss update form for staff

    if request.user.has_perm('dictionary.search_gloss'):
        update_form = GlossModelForm(instance=trans.gloss)
        video_form = VideoUploadForm(initial={'category': 'Gloss',
                                              'tag': trans.gloss.pk,
                                              'redirect': request.get_full_path()})
    else:
        update_form = None
        video_form = None

    # Regional list (sorted by dialect name) and regional template contents if this gloss has one
    regions = sorted(gloss.region_set.all(), key=lambda n: n.dialect.name)
    try:
        page = Page.objects.get(url__exact=gloss.regional_template)
        regional_template_content = mark_safe(page.content)
    except:
        regional_template_content = None

    context = {'translation': trans,
             'viewname': 'words',
             'definitions': trans.gloss.definitions(),
             'allkwds': allkwds,
             'n': n,
             'total': total,
             'matches': list(range(1, total+1)),
             'navigation': nav,
             'thumbnails': thumbnails,
             'dialect_image': map_image_for_regions(gloss.region_set),
             'regions': regions,
             'regional_template_content': regional_template_content,
             # lastmatch is a construction of the url for this word
             # view that we use to pass to gloss pages
             # could do with being a fn call to generate this name here and elsewhere
             'lastmatch': str(trans.translation)+"-"+str(n),
             'videofile': videourl,
             'update_form': update_form,
             'videoform': video_form,
             'gloss': gloss,
             'glosscount': glosscount,
             'glossposn': glossposn,
             'feedback' : True,
             'feedbackmessage': feedbackmessage,
             'tagform': TagUpdateForm(),
             'SIGN_NAVIGATION' : settings.SIGN_NAVIGATION,
             'SETTINGS_SHOW_TRADITIONAL' : settings.SHOW_TRADITIONAL,
             'SETTINGS_SHOW_FREQUENCY' : settings.SHOW_FREQUENCY,
             'DEFINITION_FIELDS' : settings.DEFINITION_FIELDS,
             }

    return render(request, "dictionary/word.html", context)

@login_required_config
def gloss(request, idgloss):
    """View of a gloss - mimics the word view, really for admin use
       when we want to preview a particular gloss"""

    if 'feedbackmessage' in request.GET:
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False

    # we should only be able to get a single gloss, but since the URL
    # pattern could be spoofed, we might get zero or many
    # so we filter first and raise a 404 if we don't get one
    can_view_not_inWeb = request.user.has_perm('dictionary.search_gloss')
    if can_view_not_inWeb:
        glosses = Gloss.objects.filter(idgloss=idgloss)
    else:
        glosses = Gloss.objects.filter(inWeb__exact=True, idgloss=idgloss)

    if len(glosses) != 1:
        raise Http404

    gloss = glosses[0]
    (glossposn, glosscount) = get_gloss_position(gloss, can_view_not_inWeb)

    # and all the keywords associated with this sign
    allkwds = gloss.translation_set.all()
    if len(allkwds) == 0:
        trans = Translation()
    else:
        trans = allkwds[0]

    videourl = gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None

    # navigation gives us the next and previous signs
    nav = gloss.navigation(request.user.has_perm('dictionary.search_gloss'))

    # the gloss update form for staff
    update_form = None

    if request.user.has_perm('dictionary.search_gloss'):
        update_form = GlossModelForm(instance=gloss)
        video_form = VideoUploadForm(initial={'category': 'Gloss',
                                              'tag': gloss.pk,
                                              'redirect': request.get_full_path()})
    else:
        update_form = None
        video_form = None

    # get the last match keyword if there is one passed along as a form variable
    if 'lastmatch' in request.GET:
        lastmatch = request.GET['lastmatch']
        if lastmatch == "None":
            lastmatch = False
    else:
        lastmatch = False

    # Regional list (sorted by dialect name) and regional template contents if this gloss has one
    regions = sorted(gloss.region_set.all(), key=lambda n: n.dialect.name)
    try:
        page = Page.objects.get(url__exact=gloss.regional_template)
        regional_template_content = mark_safe(page.content)
    except:
        regional_template_content = None

    return render(request, "dictionary/word.html",
                              {'translation': trans,
                               'definitions': gloss.definitions(),
                               'allkwds': allkwds,
                               'dialect_image': map_image_for_regions(gloss.region_set),
                               'regions': regions,
                               'regional_template_content': regional_template_content,
                               'lastmatch': lastmatch,
                               'videofile': videourl,
                               'viewname': word,
                               'feedback': True,
                               'gloss': gloss,
                               'glosscount': glosscount,
                               'glossposn': glossposn,
                               'navigation': nav,
                               'update_form': update_form,
                               'videoform': video_form,
                               'tagform': TagUpdateForm(),
                               'feedbackmessage': feedbackmessage,
                               'SIGN_NAVIGATION' : settings.SIGN_NAVIGATION,
                               'SETTINGS_SHOW_TRADITIONAL' : settings.SHOW_TRADITIONAL,
                               'SETTINGS_SHOW_FREQUENCY' : settings.SHOW_FREQUENCY,
                               'DEFINITION_FIELDS' : settings.DEFINITION_FIELDS,
                               })

def remove_crude_words(words):
    try:
        crudetag = Tag.objects.get(name='lexis:crude')
    except:
        crudetag = None
    if crudetag != None:
        crude = TaggedItem.objects.get_by_model(Gloss, crudetag)
        # remove crude words from result
        result = []
        for w in words:
            # remove word if all glosses for any translation are tagged crude
            trans = w.translation_set.all()
            glosses = [t.gloss for t in trans]
            if not all([g in crude for g in glosses]):
                result.append(w)
        words = result
    return words

def remove_words_not_belonging_to_category(words, category):
    tags = Tag.objects.filter(name=category)
    if tags.count() == 0:
        return []

    # should be just one tag
    tag = tags[0]

    result = []
    for w in words:
        trans = w.translation_set.all()
        glosses = [t.gloss for t in trans]
        for g in glosses:
            if tag in g.tags:
                if w not in result:
                    result.append(w)
    words = result

    return words

@login_required_config
def search(request):
    """Handle keyword search form submission"""

    form = UserSignSearchForm(request.GET.copy())

    if form.is_valid():

        # need to transcode the query to our encoding
        term = form.cleaned_data['query']
        category = form.cleaned_data['category']

        if term == '' and category in ['', 'all']:
            words = []
        else:

            # safe search for authenticated users if the setting says so
            safe = (not request.user.is_authenticated()) and settings.ANON_SAFE_SEARCH

            try:
                term = smart_unicode(term)
            except:
                # if the encoding didn't work this is
                # a strange unicode or other string
                # and it won't match anything in the dictionary
                words = []


            if category in ['all', '']:

                if request.user.has_perm('dictionary.search_gloss'):
                    # staff get to see all the words that have at least one translation
                    words = Keyword.objects.filter(text__istartswith=term, translation__isnull=False).distinct()
                else:
                    # regular users see either everything that's published
                    words = Keyword.objects.filter(text__istartswith=term,
                                                    translation__gloss__inWeb__exact=True).distinct()
            else:
                # might fail if category doesn't exist
                tag = Tag.objects.get(name=category)
                glosses = TaggedItem.objects.get_by_model(Gloss, tag)
                if request.user.has_perm('dictionary.search_gloss'):
                    glosses = glosses.filter(translation__translation__text__istartswith=term)
                else:
                    glosses = glosses.filter(translation__translation__text__istartswith=term,
                                             inWeb__exact=True)

                # get the keyword list that these
                # NOTE: these may now include keywords not starting with our term
                translations = glosses.values('translation__translation').order_by()
                words = []
                for tr in translations:
                    kw = Keyword.objects.get(id=tr['translation__translation'])
                    if not kw in words:
                        words.append(kw)

            if safe:
                words = remove_crude_words(words)

    else:
        term = ''
        category = 'all'
        words = []

    # display the keyword page if there's only one hit and it is an exact match
    if len(words) == 1 and words[0].text == term:
        return HttpResponseRedirect('/dictionary/words/'+words[0].text+'-1.html' )

    (result_page, paginator) = paginate(request, words, 49)

    return render(request, "dictionary/search_result.html",
                              {'query' : term,
                               'searchform': form,
                               'paginator' : paginator,
                               'wordcount' : len(words),
                               'category' : category,
                               'page' : result_page,
                               'FILTER_TAGS': getattr(settings, 'DICTIONARY_FILTER_TAGS', []),
                               'ANON_SAFE_SEARCH': getattr(settings, 'ANON_SAFE_SEARCH', True),
                               'ANON_TAG_SEARCH': getattr(settings, 'ANON_TAG_SEARCH', True),
                               'language': getattr(settings, 'LANGUAGE_NAME', 'Auslan'),
                               })


def keyword_value_list(request, prefix=None):
    """View to generate a list of possible values for
    a keyword given a prefix."""


    kwds = Keyword.objects.filter(text__startswith=prefix)
    kwds_list = [k.text for k in kwds]
    return HttpResponse("\n".join(kwds_list), content_type='text/plain')

def missing_video_list():
    """A list of signs that don't have an
    associated video file"""

    glosses = Gloss.objects.filter(inWeb__exact=True)
    for gloss in glosses:
        if not gloss.has_video():
            yield gloss

def missing_video_view(request):
    """A view for the above list"""

    glosses = missing_video_list()

    return render(request, "dictionary/missingvideo.html",
                              {'glosses': glosses})

def paginate(request, objects, npages):
    # There might be many matches, so let's paginate them...
    paginator = Paginator(objects, npages)
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
    return (result_page, paginator)

def get_gloss_position(gloss, can_view_not_inWeb):
    '''
    This functions returns a tuple; the first value
    of the tuple is the gloss's position relative
    to all of the other glosses, and the second value
    is the total number of glosses.

    If gloss_must_be_in_web is true, then only glosses
    that are in the web will be considered.
    '''
    if gloss.sn != None:
        if  can_view_not_inWeb:
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True,
                sn__lt=gloss.sn).count()+1
    else:
        glosscount = 0
        glossposn = 0
    return (glossposn, glosscount)
