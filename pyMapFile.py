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

# skip default style, it is already loaded and 
# used to make sure a user doesn't forget to set a variable in the dict
if not (options.style == 'default'):
  # load the custom style and override default.
  tempstyle = yaml.load(open('styles/' + options.style + '.yaml','r'))

  #check to see if one or more OTHER styles need to be included; load them first!
  if 'include_styles' in tempstyle:
    if (len(tempstyle['include_styles']) > 0):
      for namedstyle in tempstyle['include_styles'].split(','):
        # skip default style, it is already loaded and 
        # used to make sure a user doesn't forget to set a variable in the dict
        if not (namedstyle == 'default'):
          # load the custom style and override default.
          tempstyle2 = yaml.load(open('styles/' + namedstyle + '.yaml','r'))
          vars.update(tempstyle2)  

  vars.update(tempstyle)

style = vars

if options.full:
  #write directly to file instead of parsing the output of print..
  f = open('generated/'+ options.style + 'style.msinc', 'w')
  f.write ("###### level 0 ######")
  f.write("\n")
  for k,v in style.items():
    if type(v) is dict:
      f.write("#define _%s0 %s"%(k,v[0]))
      f.write("\n")
    else:
      f.write("#define _%s0 %s"%(k,v))
      f.write("\n")

  for i in range(1,19):
    f.write("\n")
    f.write("###### level %d ######"%(i))
    f.write("\n")
    for k,v in style.items():
      if type(v) is dict:
        if not i in v:
          f.write("#define _%s%d _%s%d"%(k,i,k,i-1))
          f.write("\n")
        else:
          f.write("#define _%s%d %s"%(k,i,v[i]))
          f.write("\n")
      else:
          f.write("#define _%s%d %s"%(k,i,v))
          f.write("\n")
  f.close()

  for i in range(19):
    f = open('generated/'+ options.style + 'level' + str(i) + '.msinc', 'w')
    for k,v in style.items():
      f.write("#undef _%s"%(k))
      f.write("\n")
    for k,v in style.items():
      f.write("#define _%s _%s%s"%(k,k,i))
      f.write("\n")
    f.close()

# Per level generation, not needed anymore, but left here for backward compatibility
if options.level != -1:
  level = options.level
  for k,v in style.items():
    print ("#undef _%s"%(k))

  for k,v in style.items():
    print ("#define _%s _%s%s"%(k,k,level))
