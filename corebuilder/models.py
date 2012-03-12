
from types import *

#from django.db import models

from CoreBuilder.settings import INSTALL_TARGETS
from backend import load_target

# Create your models here.

"""class Build(models.Model):
    pkg = models.CharField(max_length=50)
    bld_date = models.DateTimeField('date built')
    cxx = models.CharField(max_length=50)
    cc = models.CharField(max_length=50)
    cflags = models.CharField(max_length=200)

    def __unicode__(self):
        return "pkg: %s\nbuild Date: %s\nCXX: %s\ncc: %s\nCFlags: %s\n" \
                % (self.pkg, self.bld_date, self.cxx, self.cc, self.cflags)
"""
ALL = 'All'
NONE = '------- None -------'

class Pkgs(object):
    legend_keys = ['i', 'ver', 'slot', 'repo_name',
            'repo_path', 'hardmasked', 'unmasked',
            'keywordmasked']

    legend = {'i': 0, 'ver': 1, 'slot': 2, 'repo_name': 3,
            'repo_path': 4, 'hardmasked': 5, 'unmasked': 6,
            'keywordmasked': 7}

    def __init__(self, get_func=None, pms_lib=None):
        self._pkgs = [ALL, NONE]
        self.selected_cat = ''
        self.selected_pkg = ''
        self.selected_ver = ''
        self.shown_versions = []
        self.pms_lib = pms_lib

        if get_func:
            try:
                self._pkgs += get_func()
            except Exception as e:
                print("Pkgs.__init__(); exception from get_func():\n", e)

    def select(self, cat=ALL, include_versions=False):
        #print "Pkgs.select(), self=", self
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
                        print("p.split('/') error p=", p)
        else:
            pkgs = set()
            for p in self._pkgs:
                if p not in [ALL, NONE]: # and cat in p
                    pkgs.add(p)
            pkgs = sorted(pkgs)
        #print "Pkgs.select(), len pkgs=", len(pkgs)

        self.selected_cat = cat
        return pkgs


    def versions(self, cp):
        self.shown_versions = []
        try:
            self.shown_versions = self.pms_lib.get_versions(cp, include_masked = True)
            self.shown_versions.sort(reverse=True)
        except Exception as e:
            print("Pkgs.versions: error from self.pms_lib.\n", e)
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


class Categories(object):

    def __init__(self):
        self._categories = [NONE, ALL]

    def __unicoide__(self):
        return "%s" % ', '.join(self._categories)

    def _populate(self, pkgs):
        newcats = set()
        for pkg in pkgs:
            newcats.add(pkg.split("/")[0])
        self._categories = [NONE, ALL] + list(newcats)

    def get(self):
        return sorted(self._categories)


class Views(object):
    """controls the information display according to the
    selected view
    """
    _views = ["-- Select --", "Trees", "Installed", "Not_Installed"]

    def __init__(self, target_name=None):
        self.pkgs = {
            "-- Select --": Pkgs(),
            "Trees": None,
            "Installed": None,
            "Not_Installed": None
        }
        self.cats = {
            "Trees": None,
            "Installed": None,
            "Not_Installed": None
        }
        self.selected = ""

        if target_name:
            self.target_name = target_name
            self.pms_instance = load_target(target_name)
            self.pms_lib = self.pms_instance.pms_lib

    def all(self):
        return sorted(self._views)

    def select(self, view):
        print("Views.select():", view)
        if view in ["-- Select --"]:
            _cats = [NONE]
        elif view in ["Trees", "Installed", "Not_Installed"]:
            print("Views.select(): made it here :)")
            cat = getattr(self, view)()
            if cat:
                _cats = cat.get()
            else:
                _cats = ["-- ERROR --"]
        else:
            _cats = cats.get()
        print("Views.select():", view, self.pkgs[view], len(self.pkgs[view]._pkgs))
        return (_cats, self.pkgs[view].select('All'))

    def Trees(self):
        if not self.cats["Trees"]:
            print("Views.Trees(), new Trees lists"), self.pms_instance
            self.pkgs["Trees"] = Pkgs(self.pms_lib.get_allnodes, self.pms_lib)
            print("Views.Trees(), pks length = ", self.pkgs["Trees"], len(self.pkgs["Trees"]._pkgs))
            self.cats["Trees"] = Categories()
            self.cats["Trees"]._populate(self.pkgs["Trees"].select())
            print("Views.Trees(), cats length = ", len(self.cats["Trees"]._categories))
        return self.cats["Trees"]

    def Installed(self):
        if not self.cats["Installed"]:
            print("Views.Installed(), new Installed lists"), self.pms_instance
            self.pkgs["Installed"] = Pkgs(self.pms_lib.get_installed_list, self.pms_lib)
            print("Views.Installed(), pks length = ", self.pkgs["Installed"], len(self.pkgs["Installed"]._pkgs))
            self.cats["Installed"] = Categories()
            self.cats["Installed"]._populate(self.pkgs["Installed"].select())
            print("Views.Installed(), cats length = ", len(self.cats["Installed"]._categories))
        return self.cats["Installed"]

    def Not_Installed(self):
        if not self.cats["Not_Installed"]:
            ct, pt = self.select("Trees")
            ci, pi = self.select("Installed")
            try:
                print("Views.Not_Installed(), new Not_Installed lists")
                spt = set(pt)
                print(len(spt))
                spi = set(pi)
                print(len(spi))
                print()
                pkgset = spt.difference(spi)
                print(len(pkgset))
                self.pkgs["Not_Installed"] = Pkgs(pms_lib=self.pms_lib)
                self.pkgs["Not_Installed"]._pkgs = list(pkgset)
            except Exeption as e:
                print("Views.Not_Installed(), Exeption", e)

            print("Views.Not_Installed(), pks length = ", len(self.pkgs["Not_Installed"]._pkgs))
            self.cats["Not_Installed"] = Categories()
            self.cats["Not_Installed"]._populate(self.pkgs["Not_Installed"].select())
            print("Views.Not_Installed(), cats length = ", len(self.cats["Not_Installed"]._categories))
        return self.cats["Not_Installed"]

    @property
    def pkg_legend(self):
        return self.pkgs["-- Select --"].legend

    @property
    def pkg_legend_keys(self):
        return self.pkgs["-- Select --"].legend_keys


#pkgviews = Views()

print("MODELS initialized")

