def count_tags(filename):
    """
    counts the number of tags within the XML filename and 
    returns a dictionary of tags and the total count of each tag type found.
    """
    tags = {}
    for ev, element in ET.iterparse(filename):
        tag = element.tag
        if tag not in tags.keys():
            tags[tag] = 1
        else:
            tags[tag] = tags[tag]+1
    return tags
    
    
lower = re.compile(r'^([a-z]|_)*$')  # tags that contain ONLY lowercase letters and are valid.
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$') # tags that are valid but with a colon.
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]') # tags with problematic characters.  

def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        if lower.match(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.match(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.match(element.attrib['k']):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1  # other for tags that do not fall into the other three categories.
            
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys
