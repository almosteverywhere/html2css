##!/usr/bin/python
## html2css takes an html file, and optionally an existing css file, and writes out "property {}" stubs for css selectors that don't already exist in the file. I was basically sick of
## typing out all the stupid divs by hand, I don't know why my editor doesn't just do this automatically anyways.
## NOTE: it doesn't add stubs for tags like <body>, etc, just divs. 
## script that takes an existing html file, css file and writes out stubs for css selectors that don't already exist in the css


import sys
import re
import string

def html2css(htmlfile, cssfile, outputfile):
  f = open(htmlfile, 'r')
  file_contents = f.read()
  new_css_table = []
  
  # ok this gives us a table of existing css selectors and rules
  # we're only going to look at this table to see if something already exists in the css file, but we dont' write out this table anymore
  # we're just going to write at the end of the existing css file.'
  
  #ok let's look at this step
  css_dict = build_css_dict(cssfile,outputfile) 
  
  
  # get all the ids from the html file
  tags = re.findall(r'<div id=\"([\w-]*)"', file_contents)

  # now check it exists in the table..if so, don't write a rule
  # if not, then write a stub in the table at the end
  # we'll print out the dict at the end, with empty rules at the end for editing
  for tag in tags:
    # the tags in the dict has the . or # to indicate classes or ids so we have to add them here
    #tag = "#" + tag
    #if not (tag in css_dict):
      #print tag + "is not already in dict"
      #css_dict[tag] = "{ \n }"
    # here we're using a tuple instead of a dict because we want properties to stay in the same order as they are in the original file, and the stubs for the new 
    # properties at the end for easy access
    # you can sort the file later if you like your css in alphabetical order
    fulltag = "#" + str(tag)
    if not (fulltag in css_dict):
      print "DEBUG: fulltag not in css dict" + fulltag
      # print css_dict
      # print tag + "is already in table"  
      new_css_table.append([fulltag, "{ \n }"])
      
    # do all the classes
    
    #for key in css_dict:
      #print "key = " + key
      #print "property = " + css_dict[key]
    
  # ok this is cheap but fast
  f.close()
  f = open(htmlfile, 'r')
  file_contents = f.read()
  # print out all the class stubs
  classtags = re.findall(r'<div class=\"(\w*)"', file_contents)
  
  for tag in classtags:
    tag = string.strip(tag)
    # print tag 
    #if not (tag in css_dict):
      ## print tag + "is already in dict"
      #css_dict[tag] = "{ \n }"
    # here we're using a tuple instead of a dict because we want properties to stay in the same order as they are in the original file, and the stubs for the new 
    # properties at the end for easy access
    # you can sort the file later if you like your css in alphabetical order
    if not ("." + tag in css_dict):
      new_css_table.append(["." + tag, "{ \n }"])
  
    # write the table of existing css + stubs to the outputfile 
    outputf = open(outputfile, 'w')
    f = open(cssfile, 'r')
    orig_contents = f.read()    
    # first write out the original css file
    # we just write the original contents to another file so we don't accidentally clobber the original file
    outputf.write(orig_contents)


    for t in new_css_table:
      s = t[0] + t[1] + "\n"
      outputf.write(s)
     # k we done 
  return

# given a css file, build a dict of existing properties and return it
def build_css_dict(cssfile, outputfile):
  #print "in css table"
  css_dict = {}
  f = open(cssfile, 'r')
  # w = open(outputfile, 'w')
  file_contents = f.read()
  # print cssfile
  # print file_contents
  # we're matching on stuff that looks like this, let's assume it's one thing per declaration for now
  # .fbEmu a.fbEmuTitleBodyImageLink{text-decoration:none}
  # ok let's match all ids for now '
  # properties = re.findall(r'(\.\w+){(.*)}', file_contents)
  # ok, this matches a whole line before a property list, possibly multiple classes
  #classproperties = re.findall(r'(\.[\w \.]+)({.*})', file_contents)
  #idproperties = re.findall(r'(\#[\w \.]+)({.*})', file_contents)
  #for property in idproperties:
    #print property[0]
    #print property[1]
    
  # ok now try to match everything, including
  #   # ok now try to match everything, 
  # including   
  # body .fixedScrolling{position:fixed}
  # so really we want to match everything before { properties}
  allproperties = re.findall(r'([\w\n\# \.,:]+)({.*})', file_contents)
  
  # ok now we need to process this table, so that properties like div1, div2....get put into seperate entries, so we can do lookups later like "if blah in table"
  for p in allproperties:
    #if it contains a comma, then it's a multiple declaration'
    print "property", p 
    # is this a comma seperated list of properties we need to parse?
    match = re.search(r',',p[0])
    if match:
      #print "match"
      # this splits in the comma and gives us an array of the different selectors
      # ok good, now we need to remove any newlines
      selectors = re.split(r',', p[0])
      print p[0] + "  splits into  " + str(selectors)
      
      for s in selectors:
        #print "s before" + s
        # remove the newline from the string
        # strip newlines and whitespace, dunno why strip doesn't
        # do this in one op but it doesn't seem to'
        s = re.sub(r'\n', "", s)
        s = s.strip()
        #print s
        #print "s after" + s
        # p[0] will be the long string of selectors, p[1] is the css rules
        # we split p[0] into each individual selector by splitting on the , then we enter the same rules for each one
        # this is annoying, but we need it to be able to lookup individual properties in the table....
        
        print "DEBUG entering " + str(s) + " into dict with rule " + p[1]
        
        css_dict[s] = p[1] 
      # now that we have an array of selectors, enter each one into the table
      # print p[0] + "is a multiple declaration"
    #print css_dict
    # it didn't split, just a single property, enter it
    else: 
      # strip newlines and whitespace
      s = re.sub(r'\n', "", p[0])
      s = s.strip()
      css_dict[s] = p[1]
      print "DEBUG entering " + p[0] + " into dict with rule " + p[1]
    
  return css_dict 
  # do i need this, is a tuple the same as a dict? i don't think so'
  
  
  # hmm so i dont' think we need a dict here, coz we want the new stuff to be at the end so we can write them out at the end of the file'
  #for p in allproperties:
    #dict[p[0]] = p[1]
    #print "thingy: " + p[0]
    #print "properties: " + p[1]
  
  #for key in dict:
    #print "key = " + key
    #print "property = " + dict[key]

  # return a table of all the existing css rules
  #return dict
  # return allproperties
  
def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  #temporarily hardcode this
  
  #htmlfile = "index.html"
  ## cssfile = "stylesheet-test.css"
  #cssfile = "fb.css"
  
  ##htmlfile = args[]
  
  

  if not args:
    print 'usage: --htmlfile file --cssfile file [--outputfile] file'
    sys.exit(1)

  htmlfile = args[1]
  cssfile = args[3]
  outputfile = args[5]
  
  #print htmlfile 
  #print cssfile 
  #print outputfile

  html2css(htmlfile,cssfile,outputfile)

  ## Notice the summary flag and remove it from args if it is present.
  #summary = False
  #if args[0] == '--summaryfile':
    #summary = True
    #summaryfile = args[1]
    ##deletes the first two args
    #del args[0]
    #del args[0]
    
    #print args
    #f = open(summaryfile, 'w')
  ##next file is the summaryfile we want to give
  ## else: filename = args[0]
  
  #for file in args:
    #list = extract_names(file)
    #for var in list:
      #if(summary): f.write(str(var) + "\n")
      #else: print var
  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  #extract_names(filename)
  
if __name__ == '__main__':
  main()
