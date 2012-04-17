##!/usr/bin/python
## html2css takes an html file, and optionally an existing css file, and writes out "property {}" stubs for css selectors that don't already exist in the file. I was basically sick of
## typing out all the stupid divs by hand, I don't know why my editor doesn't just do this automatically anyways.
## NOTE: it doesn't add stubs for tags like <body>, etc, just divs. 
## script that takes an existing html file, css file and writes out stubs for css selectors that don't already exist in the css


import sys
import re
import string

def html2css(htmlfile, cssfile, outputfile):
  
  new_css_table = []
  css_dict = {}
  
  f = open(htmlfile, 'r')
  file_contents = f.read()
        
    # this gives us a table of existing css selectors and rules to look up if something already exists in the css file so we don't clobber existing rules
  if cssfile:   
    css_dict = build_css_dict(cssfile,outputfile) 
    
  # get all the ids from the html file, there's probably a better way to get all the ids and classes at once, but we're just doing two passes,
  # change this if performance becomes an issue
  tags = re.findall(r'<div id=\"([\w-]*)"', file_contents)

  # now check it exists in the table..
  # if not, then write a stub in the table at the end
  for tag in tags:
    # the tags in the dict has the . or # to indicate classes or ids so we have to add them here
    
    # here we're using a tuple instead of a dict because we want properties to stay in the same order as they are in the original file, and the stubs for the new 
    # properties at the end for easy access
    # you can sort the file later if you like your css in alphabetical order
    fulltag = "#" + str(tag)
    if not (fulltag in css_dict): 
      new_css_table.append([fulltag, "{ \n }"])
      
  # ok this is cheap but fast
  f.close()
  f = open(htmlfile, 'r')
  file_contents = f.read()
  # print out all the class stubs
  classtags = re.findall(r'<div class=\"(\w*)"', file_contents)
  
  for tag in classtags:
    tag = string.strip(tag)
    
    if not ("." + tag in css_dict):
      new_css_table.append(["." + tag, "{ \n }"])
      
    # first write out the original css file
    # we just write the original contents to another file so we don't accidentally clobber the original file
    
    outputf = open(outputfile, 'w')
    if cssfile:
      f = open(cssfile, 'r')
      orig_contents = f.read()    
      
      outputf.write(orig_contents)

    for t in new_css_table:
      s = t[0] + t[1] + "\n"
      outputf.write(s)
     # k we done 
  return

# given a css file, build a dict of existing properties and return it
def build_css_dict(cssfile, outputfile):

  css_dict = {}
  f = open(cssfile, 'r')
  file_contents = f.read()
    
  # we match everything before { properties}
  allproperties = re.findall(r'([\w\n\# \.,:]+)({.*})', file_contents)
  
  # now we need to process this table, so that properties like div1, div2....get put into seperate entries, so we can do lookups later like "if blah in table"
  for p in allproperties:
    #if it contains a comma, then it's a multiple declaration'
    # print "property", p 
    # is this a comma seperated list of properties we need to parse?
    match = re.search(r',',p[0])
    
    if match:
      # this splits in the comma and gives us an array of the different selectors
      selectors = re.split(r',', p[0])
      # print p[0] + "  splits into  " + str(selectors)
      
      for s in selectors:
        # strip newlines and whitespace, dunno why strip doesn't
        # do this in one op but it doesn't seem to'
        s = re.sub(r'\n', "", s)
        s = s.strip()
        # we split p[0] into each individual selector by splitting on the , then we enter the same rules for each one
        # this is annoying, but we need it to be able to lookup individual properties in the table....        
        
        css_dict[s] = p[1] 
    # it didn't split, just a single property, enter it
    else: 
      # strip newlines and whitespace
      s = re.sub(r'\n', "", p[0])
      s = s.strip()
      css_dict[s] = p[1]
      # print "DEBUG entering " + p[0] + " into dict with rule " + p[1]
    
  return css_dict 
  
def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  ##htmlfile = args[]

  if not args:
    print 'usage: [--cssfile file] htmlfile outputfile '
    sys.exit(1)
    
  # we could check that the arguments exist, and that we're not clobbering an existing css file
  # but since it's a script we're not going to use that often we're going to be lazy
  # also we could just omit --htmlfile --cssfile, etc, but it helps us keep the order of the arguments
  # straight to type it out explicitly. 

  cssfile = ''
  if args[0] == '--cssfile':
    cssfile = args[1]
    del args[0:2]
    
  if len(args) == 0:
    print "error: you must specify an html file and an output file"
    sys.exit(1)

  htmlfile = args[0]
  del args[0]
  
  if len(args) == 0:
    print "error: you must specify an output file"
    sys.exit(1)
    
  outputfile = args[0]

  html2css(htmlfile,cssfile,outputfile)

  
if __name__ == '__main__':
  main()
