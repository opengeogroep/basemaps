import sys
from optparse import OptionParser
import yaml

#Load everything from default
layer_suffixes = yaml.load(open('defaults/layer_suffixes.yaml','r'))
maxscales = yaml.load(open('defaults/maxscales.yaml','r'))
minscales = yaml.load(open('defaults/minscales.yaml','r'))
default = yaml.load(open('defaults/default.yaml','r'))
vars= {
  'layer_suffix':layer_suffixes,
  'maxscales':maxscales,
  'minscales':minscales
}
vars.update(default)
# TODO: Complete it!

#Load the style overide and the styles set
# TODO: Needs to be invoked
styles = yaml.load(open('defaults/styles.yaml','r'))
styles.update({'default':{}})
style_aliases = yaml.load(open('defaults/style_aliases.yaml','r'))

parser = OptionParser()
parser.add_option("-l", "--level", dest="level", type="int", action="store", default=-1,
  help="generate file for level n")
parser.add_option("-g", "--global", dest="full", action="store_true", default=False,
  help="generate global include file")
parser.add_option("-s", "--style", action="store", dest="style", default="default",
  help="comma separated list of styles to apply (order is important)")

(options, args) = parser.parse_args()

items = dict(vars.items())

for namedstyle in style_aliases[options.style].split(','):
  items.update(styles[namedstyle].items())
   
style = items
print (items)
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

