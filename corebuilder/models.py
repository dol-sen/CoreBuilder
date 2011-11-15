
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

ALL = '-------- All --------'
NONE = '------- None -------'

class Pkgs(object):
    _pkgs = [NONE,
        "cat-one/pkg1-1.2.0",
        "cat-one/pkg1-1.2.1",
        "cat-one/pkg2-1.2.0",
        "cat-one/pkg8-1.2.0",
        "cat-one/pkg9-1.2.0",
        "cat-one/pkg10-1.2.0",
        "cat-one/pkg11-1.2.0",
        "cat-two/pkg3-1.0.0",
        "cat-two/pkg4-1.0.0",
        "cat-two/pkg5-1.0.0",
        "cat-two/pkg6-1.0.0",
        "cat-two/pkg7-1.0.0",
    ]
    selected_cat = ALL
    selected_pkg = ''
    selected_ver = ''


    def select(self, cat=ALL):
        if cat in ["All", ALL]:
            pkgs = self._pkgs[:]
            #pkgs = [p.split('/')[1] for p in self._pkgs]
        else:
            pkgs = [NONE]
            for p in self._pkgs:
                if p not in [ALL, NONE] and cat in p:
                    try:
                        pkgs.append(p.split('/')[1])
                    except:
                        print "p.split() errorp=", p
        self.selected_cat = cat
        return pkgs


pkgs = Pkgs()

class Categories(object):
    _categories = [ALL, "cat-one", "cat-two", "cat-three"]

    def __unicoide__(self):
        return "%s" % ', '.join(self._categories)

    def _populate(self):
        pass
        #self._categories =

    def all(self):
        return sorted(self._categories)


cats = Categories()

class Packages(models.Model):
    pkg = models.CharField(max_length=50)


class Views(object):
    """controls the information display according to the
    selected view
    """
    _views = ["All", "Installed", "Not Installed"]
    selected = "All"

    def all(self):
        return sorted(self._views)

views = Views()
