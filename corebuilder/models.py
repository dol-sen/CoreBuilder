
from django.db import models

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
    _pkgs = [NONE,
        "cat-one/pkg1-1.2.0",
        "cat-one/pkg1-1.2.1",
        "cat-one/pkg2-1.2",
        "cat-one/pkg8-1.8.0",
        "cat-one/pkg9-1.2.0",
        "cat-one/pkg10-1.2.10",
        "cat-one/pkg11-1.2.11",
        "cat-two/pkg3-1.0.3",
        "cat-two/pkg4-1.0.4",
        "cat-two/pkg5-1.0.5",
        "cat-two/pkg6-1.0.6",
        "cat-two/pkg7-1.0.7",
    ]
    selected_cat = ''
    selected_pkg = ''
    selected_ver = ''


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
                    pkgs.add(p.rsplit('-', 1)[0])
            pkgs = sorted(pkgs)
        #print len(pkgs), pkgs

        self.selected_cat = cat
        return pkgs


    def versions(self, cp):
        vers = []
        for cpv in self._pkgs:
            cps = cpv.rsplit('-', 1)
            if cp == cps[0]:
                vers.append(cps[1])
        return sorted(vers)


pkgs = Pkgs()

class Categories(object):
    _categories = [NONE, ALL, "cat-one", "cat-two", "cat-three"]

    def __unicoide__(self):
        return "%s" % ', '.join(self._categories)

    def _populate(self, pkgs):
        newcats = set()
        for pkg in pkgs:
            newcat.add(pkg.split("/")[0])
        self._categories = list(newcats)

    def get(self):
        return sorted(self._categories)


cats = Categories()

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
