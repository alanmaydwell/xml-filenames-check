#!/usr/bin/env python

"""Simple check of whether filenames listed within XLM files are 
actually present in directory.

- Finds all xml files in same directory as itself
- For each one finds all filename values between  <filename> </filename> tags
- Checks whether the retrieved filenames are actually present in the dirctory
- Prints details of files listed in the xml file and those listed but not
  present.
  
Note this just uses string handling to extract details from the xml.
Might be more reliable to use XML parser instead.
"""

import os

def get_tag_values(text, tag):
    """Extract content between all instances of specified tag within string
    and return a list holding values found.
    Args:
        text - string to be examined
        tag - tag to be searched for, without "<" & ">" parts (e.g. "filename") 
    Returns:
        list holding extracted text 
    """
    tag_start = "<"+ tag +">"
    tag_end = "</" + tag +">"
    offset = len(tag_start)
    values = []
    startpos = 0

    while startpos!=-1:
        #Search for start tag in text (from start or last found position)
        # -1 returned indicates "not found"
        startpos = text.find(tag_start, startpos)
        # If found do more
        if startpos != -1:
            # Find end tag position
            endpos = text.find(tag_end, startpos+offset)
            # Extract text from between start and end tags
            values.append(text[startpos+offset:endpos])
            #Shift new starting position to the old end position
            startpos = endpos
    return values


# Get filenames present in directory
file_dir = os.getcwd()
files_present = os.listdir(file_dir)
# Extract filenames with .xml file extenction
xmls = [f for f in files_present if f.lower().endswith(".xml")]

print "*XML Filelist Check*\n"

#Examine each xml file
for xml_filename in xmls:
    with open(xml_filename, "r") as xmlfile:
        xmltext = xmlfile.read()
        #Find filenames recorded within the file
        listed_files = get_tag_values(xmltext, "filename")
        print xml_filename
        print "Files listed in xml file:", ", ".join(listed_files)  
        #Find any listed files not present in directory filelisting 
        # (sets are convenient way of determining  differences)
        files_missing = list( set(listed_files) - set(files_present) )
        #Print findings
        if files_missing:
            print "FAIL - files not found:", ", ".join(files_missing)
        else:
            print "PASS - all found in directory.\n"
        