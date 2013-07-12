import sys
from optparse import OptionParser
import yaml

#Load settings
layer_suffixes = yaml.load(open('default/layer_suffixes.yaml','r'))
maxscales = yaml.load(open('default/maxscales.yaml','r'))
minscales = yaml.load(open('default/minscales.yaml','r'))
default = yaml.load(open('default/default.yaml','r'))
vars = {
  'layer_suffix':layer_suffixes,
  'maxscale':maxscales,
  'minscale':minscales
}

#load the default style into the dictionary
vars.update(default)

parser = OptionParser()
parser.add_option("-l", "--level", dest="level", type="int", action="store", default=-1,
  help="generate file for level n")
parser.add_option("-g", "--global", dest="full", action="store_true", default=False,
  help="generate global include file")
parser.add_option("-s", "--style", action="store", dest="style", default="default",
  help="comma separated list of styles to apply (order is important)")

(options, args) = parser.parse_args()

for namedstyle in options.style.split(','):
  # skip default style, it is already loaded and 
  # used to make sure a user doesn't forget to set a variable in the dict
  if not (namedstyle == 'default'):
    # load the custom style and override default.
    tempstyle = yaml.load(open('styles/' + namedstyle + '.yaml','r'))
    vars.update(tempstyle)

style = vars

if options.full:
  print ("###### level 0 ######")
  for k,v in style.items():
    if type(v) is dict:
      print ("#define _%s0 %s"%(k,v[0]))
    else:
      print ("#define _%s0 %s"%(k,v))

  for i in range(1,19):
    print ()
    print ("###### level %d ######"%(i))
    for k,v in style.items():
      if type(v) is dict:
        if not i in v:
          print ("#define _%s%d _%s%d"%(k,i,k,i-1))
        else:
          print ("#define _%s%d %s"%(k,i,v[i]))
      else:
          print ("#define _%s%d %s"%(k,i,v))
            
if options.level != -1:
  level = options.level
  for k,v in style.items():
    print ("#undef _%s"%(k))

  for k,v in style.items():
    print ("#define _%s _%s%s"%(k,k,level))

