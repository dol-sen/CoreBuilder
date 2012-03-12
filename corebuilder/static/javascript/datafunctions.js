function populateCats(cats)
{

    var cat_select = document.getElementById("Cat_select")

    cat_select.options.length = 0;
    cat_select.options[0] = new Option(cats[0]);

    for( var i=1; i<cats.length; i++ )
    {
        cat = cats[i];
        cat_select.options[i] = new Option(cat);
    }
    if(cat_select.options.length == 0)
    {
        cat_select.options[0] = new Option(cats[0]);
    }
    cat_select.selectedIndex = 0;
    x = populatePkgs();
}

function populatePkgs()
// Populates the "Packages" selector for the selected "Category"
// from the pkgs variable previously downloaded.
{
    var cat_select = document.getElementById("Cat_select")
    var catStr = cat_select.options[cat_select.selectedIndex].value;

    var pkg_select = document.getElementById("Pkg_select");
    pkg_select.options.length = 0;
    pkg_select.options[0] = new Option(NONE);

    if(catStr == ALL)
    {
        for( var i=1; i<pkgs.length; i++ )
        {
            pkg_select.options[i] = new Option(pkgs[i]);
        }
    }
    if(catStr != NONE)
    {
        x = 1;
        for( var i=0; i<pkgs.length; i++ )
        {
            ps = pkgs[i].split("/");
            if( ps[0] == catStr )
            {
                pkg_select.options[x] = new Option(ps[1]);
                x++;
            }
        }
    }
    x = populateVer([])
}

function populateVer(vers)
// Populates the "Versions" selector with the passed in version list
{

    var ver_select = document.getElementById("Ver_select")

    ver_select.options.length = 0;
    ver_select.options[0] = new Option(NONE);

    for( var i=0; i<vers.length; i++ )
    {
        ver_select.options[i+1] = new Option(vers[i]);
    }
    // Now reset the detail view
    var x = removeSubnodes(document.getElementById("pkg_detail"));
}

function build_versions()
// builds list of string representations of the ebuild versions
// to add to the version selector
{
    var vers = [];
    var max_v = 0;
    var max_s = 4;

    var data = [];
    var ver = '';
    var slot = '';
    var repo = '';
    var pad = "_";
    var v_str = String;

    // determine max lengths
    for ( var i=0; i<versions_data.length; i++ )
    {
        data = versions_data[i];
        ver = data[1];
        slot = data[2];
        max_v = Math.max(max_v, ver.length);
        max_s = Math.max(max_s, slot.length);
    };

    // create the padded string
    for ( var i=0; i<versions_data.length; i++ )
    {
        data = versions_data[i];
        ver = data[1];
        slot = data[2];
        repo = data[3];
        v_str = ver.padRight(max_v+1, pad).concat(
            ' | ', slot.padCenter(max_s, pad), ' | ', repo);
        vers.push(v_str)
    }
    return vers;
}


function keys(obj)
// returns a list of keys in the object
{
    var keys = [];
    for(var key in obj)
    {
        keys.push(key);
    }
    return keys;
}

function removeSubnodes(node)
{
    // Remove the old list items if they exist
    while(node.firstChild) node.removeChild(node.firstChild);
}

function tabHeader(tab)
{
        myElement = document.createElement("h1");
        myElement.innerHTML = current_pkg;
        tab.appendChild(myElement);
}

function displayMeta(parent, metaobj)
// Display the metadata information for the selected cat/pkg-ver
{
    var _keys = keys(metaobj);
    var key = '';
    var val = '';
    for( var i=0; i<_keys.length; i++ )
    {
        key = _keys[i];
        val = String(metaobj[key]).split(",").join(", ");
        myElement = document.createElement("li");
        myElement.innerHTML = "<b>"+key + ": " +"</b>" + val;
        parent.appendChild(myElement);
    }
}

function displaySummary(cpv, metaobj)
// Display the metadata information for the selected cat/pkg-ver
{
    var detail = document.getElementById("pkg_detail");
    var x = removeSubnodes(detail);
    if(cpv)
    {
        tabHeader(detail);
        displayMeta(detail, metaobj);
    }
}

function displayDeps(cpv, metaobj)
// Display the dependency graph
{
    var detail = document.getElementById("pkg_deps");
    var x = removeSubnodes(detail);
    if(cpv)
    {
        tabHeader(detail);
        displayMeta(detail, metaobj);
    }
    tabs_loaded['deps'] = true;
}

function displayChglog(cpv, metaobj)
// Display the ChangeLog
{
    var detail = document.getElementById("pkg_chglog");
    var x = removeSubnodes(detail);
    if(cpv)
    {
        tabHeader(detail);
        displayMeta(detail, metaobj);
    }
    tabs_loaded['chglog'] = true;
}

function displayInst_files(cpv, metaobj)
// Display the installed files list
{
    var detail = document.getElementById("pkg_inst_files");
    var x = removeSubnodes(detail);
    if(cpv)
    {
        tabHeader(detail);
        displayMeta(detail, metaobj);
    }
    tabs_loaded['inst_files'] = true;
}

function displayEbuild(cpv, metaobj)
// Display the ebuild
{
    var detail = document.getElementById("pkg_ebuild");
    var x = removeSubnodes(detail);
    if(cpv)
    {
        tabHeader(detail);
        displayMeta(detail, metaobj);
    }
    tabs_loaded['ebuild'] = true;
}

function displayUse(cpv, metaobj)
// Display the use flag widget
{
    var detail = document.getElementById("pkg_use");
    var x = removeSubnodes(detail);
    if(cpv)
    {
        tabHeader(detail);
        displayMeta(detail, metaobj);
    }
    tabs_loaded['use'] = true;
}

function displayConfig(cpv, metaobj)
// Display the config files for editing
{
    var detail = document.getElementById("pkg_cflags");
    var x = removeSubnodes(detail);

    if(cpv)
    {
        tabHeader(detail);
        displayMeta(detail, metaobj);
    }
    tabs_loaded['cflags'] = true;
}

function debug(){
    var detail = document.getElementById("debug");
    var x = removeSubnodes(detail);
}

function getTarget()
// Ajax call. Gets the categories and packages lists for the
// selected view and then populates the "Categories" selector
{
    $.getJSON("targetchanged/",
        {
            target: this.options[this.selectedIndex].value,
            format: "json"
        },
            function(json)
            {
                if (json['success'] == false){
                    var message = "Target selector Failed to get the" +
                        " target views, categories and pkgs data\n\n";
                    alert(message + json['views'] + "\n\n" +
                        json['categories'] + "\n\n" +
                        json['pkgs']);
                };
                pkgs = json['pkgs'];
                ret = populateCats(json['categories']);
                alert("NEW categories: " + String(json['categories'].length) +
                    " pkgs: " + String(pkgs.length));
            }
    );
}


function getPkgs()
// Ajax call. Gets the categories and packages lists for the
// selected view and then populates the "Categories" selector
{
    $.getJSON("viewchanged/",
        {
            view: this.options[this.selectedIndex].value,
            format: "json"
        },
            function(json)
            {
                if (json['success'] == false){
                    var message = "View selector Failed to get the" +
                        " selected views categories and pkgs data\n\n";
                    alert(message + json['categories'] + "\n\n" + json['pkgs']);
                };
                pkgs = json['pkgs'];
                ret = populateCats(json['categories']);
                alert("NEW categories: " + String(json['categories'].length) +
                    " pkgs: " + String(pkgs.length));
            }
    );
}

function getVers()
// Ajax call.  Gets the version list for the selected cat/pkg
// and then populates the Versions selector.
{
    var sel_pkg = this.options[this.selectedIndex].value;
    if(sel_pkg == NONE)
    {
        var ret = populateVer([]);
        return;
    }

    var cat_select = document.getElementById("Cat_select");
    var sel_cat = cat_select.options[cat_select.selectedIndex].value;
    if(sel_cat == ALL)
    {
        // check for cat/pkg entry
        var sp = sel_pkg.split("/");
        if(sp.length >1)
        {
            sel_pkg = sp[1];
            sel_cat = sp[0];
        }
    }

    $.getJSON("pkgchanged/",
        {
            cat: sel_cat,
            pkg: sel_pkg,
            format: "json"
        },
            function(json)
            {
                if (json['success'] == false){
                    var message = "pkg selector Failed to get the" +
                        " package versions data for:\n\n";
                    alert(message + json['cp'] + "\n\n" + json['versions']);
                };
                versions_data = json['versions'];
                //versions_legend = json['legend'];
                //displayConfig(json['cp'], json['versions'])
                vers = build_versions();
                ret = populateVer(vers);
            }
    );
}

function getMeta()
// Ajax call. Gets the cat/pkg-ver metadata for display in "Package Detail"
{
    if(this.selectedIndex == 0)
    {
        var x = removeSubnodes(document.getElementById("pkg_detail"));
        current_pkg = "";
        return;
    }
    var v_index = this.selectedIndex-1;
    var v_data = versions_data[v_index];
    var selected_ver = v_data[1];
    var cat_select = document.getElementById("Cat_select");
    var pkg_select = document.getElementById("Pkg_select");
    $.getJSON("verchanged/",
        {
            cat: cat_select.options[cat_select.selectedIndex].value,
            pkg: pkg_select.options[pkg_select.selectedIndex].value,
            ver: selected_ver,
            index: v_index,
            format: "json"
        },
            function(json)
            {
                if (json['success'] == false){
                    var message = "version selector Failed to get the" +
                        " package metadata data for:\n\n";
                    alert(message + json['cpv'] + "\n\n" + json['meta']);
                };
                current_pkg = json['cpv'];
                ret = displaySummary(json['cpv'], json['meta']);
            }
    );
}

function getDeps(){
    // Ajax call.  Gets the dependency tree

    if (tabs_loaded["deps"]){
        return;
    };
    data = {"module": "NotImplemented"};
    displayDeps(current_pkg, data);
}

function getChglog(){
    // Ajax call.  Gets the ChangeLog

    if (tabs_loaded["chglog"]){
        return;
    };
    data = {"module": "NotImplemented"};
    displayChglog(current_pkg, data);
}

function getInst_files(){
    // Ajax call.  Gets the installed files list

    if (tabs_loaded["inst_files"]){
        return;
    };
    data = {"module": "NotImplemented"};
    displayInst_files(current_pkg, data);
}

function getEbuild(){
    // Ajax call.  Gets the ebuild

    if (tabs_loaded["ebuild"]){
        return;
    };
    data = {"module": "NotImplemented"};
    displayEbuild(current_pkg, data);
}

function getUse(){
    // Ajax call.  Builds the use flag widget

    if (tabs_loaded["use"]){
        return;
    };
    data = {"module": "NotImplemented"};
    displayUse(current_pkg, data);
}

function getCflags(){
    // Ajax call.  Edit/Save the cflags, etc.

    if (tabs_loaded["cflags"]){
        return;
    };
    data = {"module": "NotImplemented"};
    displayConfig(current_pkg, data);
}

function doMerge(){
    // Ajax call. merge the selected pkg

    if (current_pkg == ''){
        return;
    };
    $.getJSON("merge/",
        {
            cpv: current_pkg,
            format: "json"
        },
            function(json)
            {
                if (json['success'] == false){
                    var message = "Merge action Failed for package:\n\n";
                    alert(message + json['cpv'] + "\n\n");
                };
            alert("Merge action started for package:'n'n" + json[cpv]);
            }
    );
}

function doUnmerge(){
    // Ajax call. unmerge the selected pkg

    if (current_pkg == ''){
        return;
    };
    $.getJSON("unmerge/",
        {
            cpv: current_pkg,
            format: "json"
        },
            function(json)
            {
                if (json['success'] == false){
                    var message = "UnMerge action Failed for package:\n\n";
                    alert(message + json['cpv'] + "\n\n");
                };
            alert("UnMerge action started for package:'n'n" +json[cpv])
            }
    );
}

