

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
#from django.error import MultiValueDictKeyError
from django.core.context_processors import csrf

#from django.contrib.auth.decorators import login_required

import json

# Create your views here.
from models import ALL, NONE, Views
from CoreBuilder.settings import (STATIC_URL, JS_URL, INSTALL_TARGETS,
    DEFAULT_TARGET)

#from .response import JSONResponse

print "Views: initializing default target"
target_name = DEFAULT_TARGET
loaded_views = {DEFAULT_TARGET: Views(target_name=target_name)}
target_view = loaded_views[target_name]
print "Views: default target", target_view


def home(request):
    return render_to_response('main.html',
        {
            'selected_cat': '',
            'selected_pkg': '',
            'selected_ver': '',
            'MEDIA_URL': STATIC_URL,
            'JS_URL': JS_URL,
            'views': target_view.all(),
            'selected_view': target_view.selected,
            'NONE': NONE,
            'ALL': ALL,
            'legend': target_view.pkg_legend,
            'targets': sorted(INSTALL_TARGETS),
            'selected_target': target_name,
        },
        context_instance=RequestContext(request),
        )


def target_changed(request):
    global target_name, target_view, loaded_views
    print "target_changed()", "request.method",request.method
    results = {
        'success': False,
        'categories': [NONE],
        'pkgs': [NONE]
        }
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('target'):
            target_name = GET['target']
        else:
            target_name = ''
        selected = target_view.selected
        print "Views.target_changed(), selected target:", target_name, loaded_views.keys(), target_view
        if target_name not in loaded_views:
            print("Views.target_changed() new loaded_views target:", target_name)
            loaded_views[target_name] = Views(target_name=target_name)
        target_view = loaded_views[target_name]
        target_view.selected = selected
        results['categories'], results['pkgs'] = target_view.select(
            target_view.selected)
        results['success'] = True
    print "Views.target_changed() , new target_view =", target_view.target_name, target_view
    #print "cats", results['categories']
    #print "pkgs:", results['pkgs']
    return HttpResponse(json.dumps(results), mimetype='application/json')


def view_changed(request):
    global target_view
    print "view_changed()", "request.method",request.method, "target_view =", target_view.target_name
    results = {
        'success': False,
        'categories': [NONE],
        'pkgs': [NONE]
        }
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('view'):
            target_view.selected = GET['view']
        else:
            target_view.selected = ''
        print "selected view:", target_view.selected
        results['categories'], results['pkgs'] = target_view.select(
            target_view.selected)
        results['success'] = True
    #print "cats", results['categories']
    #print "pkgs:", results['pkgs']
    return HttpResponse(json.dumps(results), mimetype='application/json')


def pkg_changed(request):
    global target_view
    print "pkg_changed()", target_view
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
            target_view.pkgs[target_view.selected].selected_pkg = cat + "/" + pkg
        else:
            target_view.pkgs[target_view.selected].selected_pkg = ''
        target_view.pkgs[target_view.selected].selected_ver = ''
        print "pkg =", target_view.pkgs[target_view.selected].selected_pkg
        results["cp"] = target_view.pkgs[target_view.selected].selected_pkg
        results['versions'] = target_view.pkgs[target_view.selected].versions(
            target_view.pkgs[target_view.selected].selected_pkg)
        results['legend'] = target_view.pkg_legend_keys
        #print results['versions']
        results['success'] = True
        return HttpResponse(json.dumps(results), mimetype='application/json')


def get_metadata(request):
    global target_view
    print "get_metadata()", target_view
    results = {
        'success': False,
        'meta': [NONE],
        'cpv': ""
        }
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('index'):
            index = int(GET['index'])
            ebuild = target_view.pkgs[target_view.selected].shown_versions[index]
    print index, ebuild
    print "cpv =", ebuild.pkg_name()
    results['success'] = True
    results['meta'] = {
        'Description': ebuild.description,
        'Long Description': ebuild.longdescription,
        'Homepages': ebuild.homepages,
        'Keywords': ebuild.keywords,
        'IUSE': ebuild.iuse,
        'License': ebuild.license,
        }
    results['cpv'] = ebuild.pkg_name()
    print results
    return HttpResponse(json.dumps(results), mimetype='application/json')


def merge(request):
    print "Views, merge()"
    results = {
        'success': False,
        'cpv': ""
        }
    if request.method == 'GET':
        GET = request.GET
        results['cpv'] = GET['cpv']
    print "cpv =", results['cpv']
    results['success'] = True
    return HttpResponse(json.dumps(results), mimetype='application/json')


def unmerge(request):
    print "Views, unmerge()"
    results = {
        'success': False,
        'cpv': ""
        }
    if request.method == 'GET':
        GET = request.GET
        results['cpv'] = GET['cpv']
    print "cpv =", results['cpv']
    results['success'] = True
    return HttpResponse(json.dumps(results), mimetype='application/json')

