
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
#from django.error import MultiValueDictKeyError

# Create your views here.
from ..corebuilder.models import Packages, cats, pkgs, ALL, NONE, views
from CoreBuilder.settings import HERE, STATIC_URL


def home(request):
    return render_to_response('main.html',
        {'categories': cats.all(),
        'selected_cat': pkgs.selected_cat,
        'packages': pkgs.select(pkgs.selected_cat),
        'selected_pkg': pkgs.selected_pkg,
        'versions': [NONE],
        'selected_ver': pkgs.selected_ver,
        'MEDIA_URL': STATIC_URL,
        'views': views.all(),
        'selected_view': views.selected,
        },
        context_instance=RequestContext(request)
        )


def cat_changed(request):
    print "cat_changed()"
    if request.method == 'POST':
        try:
            pkgs.selected_cat = request.POST['Cat_selector']
        except:
            pkgs.selected_cat = ''
        pkgs.selected_pkg = ''
        pkgs.selected_ver = ''
        return HttpResponseRedirect('/')


def pkg_changed(request):
    print "pkg_changed()"
    if request.method == 'POST':
        try:
            pkgs.selected_pkg = request.POST['Pkg_selector']
        except:
            pkgs.selected_pkg = ''
        pkgs.selected_ver = ''
        return HttpResponseRedirect('/')


def ver_changed(request):
    print "ver_changed()"
    if request.method == 'POST':
        try:
            pkgs.selected_ver = request.POST['Ver_selector']
        except:
            pkgs.selected_ver = ''
        return HttpResponseRedirect('/')


def view_changed(request):
    print "ver_changed()"
    if request.method == 'POST':
        try:
            views.selected = request.POST['View_selector']
        except:
            pkgs.selected_ver = ''
        return HttpResponseRedirect('/')
