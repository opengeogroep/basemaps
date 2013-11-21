BaseMaps for mapserver 6.2
==========================

This is a python script and c preprocessor to build a
complete mapfile from a set of templates and styling information for 
a postgis database with openstreetmap data imported with imposm3.

* the mapfiles are compatible with mapserver versions >= 6.2.0

* the build process uses the gcc preprocessor extensively, you should 
have it installed on your system. On linux, check that the 'cpp' command 
is present. On OSX, the provided 'cpp' program is a shell wrapper that 
is not suitable: the Makefile is coded to call 'cpp-4.2', which you can change in case
you have another version installed.

* The mapfiles rely on the database schema as created by a recent 
version of imposm3.

How to
------

run:
        make STYLE=<stylename

Currently, the following styles are predefined:
* default (the original style used with basemaps, inherited by the 
other styles)
* nobuildings (as default, but without openstreetmap buildings)
* bing
* centerlined
* outlined
* google
* michelin
* brt (a schema designed for public safety in the Netherlands)
* (deprecated, needs fixing) osm2pgsql.yaml

Configuration
-------------
Most configuration and tweaks should be done in:

* styles/<stylename>.yaml

If you want to create a new style, best practice is to copy default.yaml 
and change it to fit your needs.


