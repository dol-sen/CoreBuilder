

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
#from django.error import MultiValueDictKeyError

import json

# Create your views here.
from models import Packages, cats, pkgs, ALL, NONE, pkgviews
from CoreBuilder.settings import STATIC_URL, JS_URL
#from .response import JSONResponse


def home(request):
    return render_to_response('main.html',
        {
            'selected_cat': pkgs.selected_cat,
            'selected_pkg': pkgs.selected_pkg,
            'selected_ver': pkgs.selected_ver,
            'MEDIA_URL': STATIC_URL,
            'JS_URL': JS_URL,
            'views': pkgviews.all(),
            'selected_view': pkgviews.selected,
            'NONE': NONE,
            'ALL': ALL,
        },
        context_instance=RequestContext(request),
        )


def view_changed(request):
    print "view_changed()", "request.method",request.method
    results = {
        'success': False,
        'categories': [NONE],
        'pkgs': [NONE]
        }
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('view'):
            pkgviews.selected = GET['view']
        else:
            pkgviews.selected = ''
        print "selected view:", pkgviews.selected
        results['categories'], results['pkgs'] = pkgviews.select(pkgviews.selected)
        results['success'] = True
    #print "cats", results['categories']
    #print "pkgs:", results['pkgs']
    return HttpResponse(json.dumps(results), mimetype='application/json')


def pkg_changed(request):
    print "pkg_changed()"
    results = {
        'success': False,
        'versions': [NONE],
        'cp': ""
        }
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('cat') and GET.has_key('pkg'):
            cat = request.GET['cat']
            pkg = request.GET['pkg']
            pkgs.selected_pkg = cat + "/" + pkg
        else:
            pkgs.selected_pkg = ''
        pkgs.selected_ver = ''
        #print "pkg =", pkgs.selected_pkg
        results["cp"] = pkgs.selected_pkg
        results['versions'] = pkgs.versions(pkgs.selected_pkg)
        #print results['versions']
        results['success'] = True
        return HttpResponse(json.dumps(results), mimetype='application/json')


def get_metadata(request):
    print "get_metadata()"
    results = {
        'success': False,
        'meta': [NONE],
        'cpv': ""
        }
    c = p = v = ''
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('cat'):
            c = GET['cat']
        if GET.has_key('pkg'):
            p = GET['pkg']
        if GET.has_key('ver'):
            v = GET['ver']
    cpv = c + "/" + p + "-" + v
    print "cpv =", cpv
    results['success'] = True
    results['meta'] = {
        'description': "blah,blah, blah",
        'maintainer': "superdev@gentoo.org",
        'IUSE': "x, y, z"
        }
    results['cpv'] = cpv
    print results
    return HttpResponse(json.dumps(results), mimetype='application/json')


