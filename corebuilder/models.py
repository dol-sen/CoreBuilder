
from types import *

from django.db import models

from backend import pms_instance

pms_lib = pms_instance.pms_lib

# Create your models here.

class Build(models.Model):
    pkg = models.CharField(max_length=50)
    bld_date = models.DateTimeField('date built')
    cxx = models.CharField(max_length=50)
    cc = models.CharField(max_length=50)
    cflags = models.CharField(max_length=200)

    def __unicode__(self):
        return "pkg: %s\nbuild Date: %s\nCXX: %s\ncc: %s\nCFlags: %s\n" \
                % (self.pkg, self.bld_date, self.cxx, self.cc, self.cflags)

ALL = 'All'
NONE = '------- None -------'

class Pkgs(object):
    _pkgs = [ALL, NONE]
    _pkgs += pms_lib.get_allnodes()
    selected_cat = ''
    selected_pkg = ''
    selected_ver = ''
    shown_versions = []
    legend_keys = ['i', 'ver', 'slot', 'repo_name',
            'repo_path', 'hardmasked', 'unmasked',
            'keywordmasked']

    legend = {'i': 0, 'ver': 1, 'slot': 2, 'repo_name': 3,
            'repo_path': 4, 'hardmasked': 5, 'unmasked': 6,
            'keywordmasked': 7}


    def select(self, cat=ALL, include_versions=False):
        if cat in ["All", ALL] and include_versions:
            pkgs = self._pkgs[:]
            #pkgs = [p.split('/')[1] for p in self._pkgs]
        elif cat not in ["All", ALL] and not include_versions:
            pkgs = [NONE]
            for p in self._pkgs:
                if p not in [ALL, NONE] and cat in p:
                    try:
                        pkgs.append(p.split('/')[1])
                    except:
                        print "p.split('/') error p=", p
        else:
            pkgs = set()
            for p in self._pkgs:
                if p not in [ALL, NONE]: # and cat in p
                    pkgs.add(p)
            pkgs = sorted(pkgs)
        #print len(pkgs), pkgs

        self.selected_cat = cat
        return pkgs


    def versions(self, cp):
        self.shown_versions = pms_lib.get_versions(cp, include_masked = True)
        self.shown_versions.sort(reverse=True)
        vers = []
        i = 0
        for cpv in self.shown_versions:
            vers.append(self.build_ver_list(cpv, i))
            i += 1
        return vers

    def build_ver_list(self, cpv, i):
        ver = cpv.get_version()
        slot = cpv.slot
        ovl_path = cpv.repo_path
        if type(ovl_path) is IntType: # catch obsolete
            ovl_path = "Ebuild version no longer supported"
            ovl_label = "Obsolete"
        elif "/packages" in ovl_path:
            ovl_label = "Packages"
        else:
            ovl_label = cpv.repo_name
        data = [i, ver, cpv.slot, ovl_label, ovl_path, cpv.hardmasked,
            cpv.unmasked, cpv.keywordmasked]
        return data


pkgs = Pkgs()

class Categories(object):
    _categories = [NONE, ALL]

    def __unicoide__(self):
        return "%s" % ', '.join(self._categories)

    def _populate(self, pkgs):
        newcats = set()
        for pkg in pkgs:
            newcats.add(pkg.split("/")[0])
        self._categories = [NONE, ALL] + list(newcats)

    def get(self):
        return sorted(self._categories)


cats = Categories()
cats._populate(pkgs.select())

class Packages(models.Model):
    pkg = models.CharField(max_length=50)


class Views(object):
    """controls the information display according to the
    selected view
    """
    _views = ["-- Select --", "All", "Installed", "Not Installed"]
    selected = ""

    def all(self):
        return sorted(self._views)

    def select(self, view):
        #print "Views.select():", view
        if view in ["-- Select --"]:
            _cats = [NONE]
        else:
            _cats = cats.get()
        #print "Views.select():", _cats
        return (_cats, pkgs.select('All'))

pkgviews = Views()
