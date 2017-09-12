OSMFILE = "sample_sf.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
num_line_street_re = re.compile(r'\d0?(st|nd|rd|th|)\s(Line)$', re.IGNORECASE) # Spell lines ten and under
nth_re = re.compile(r'\d\d?(st|nd|rd|th|)', re.IGNORECASE)
nesw_re = re.compile(r'\s(North|East|South|West)$')


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Circle", "Crescent", "Gate", "Terrace", "Grove", "Way"]

mapping = { 
            "St": "Street",
            "St.": "Street",
            "st": "Street",
            "STREET": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Ave,": "Avenue",
            "ave": "Avenue",
            "ave.": "Avenue",
            "ave,": "Avenue",
            "Dr.": "Drive",
            "Dr": "Drive",
            "Rd": "Road",
            "Rd.": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Blvd,": "Boulevard",
            "blvd": "Boulevard",
            "blvd.": "Boulevard",
            "blvd,": "Boulevard",
            "Ehs": "EHS",
            "Trl": "Trail",
            "Cir": "Circle",
            "Cir.": "Circle",
            "Ct": "Court",
            "Ct.": "Court",
            "Ctr": "Center",
            "Ctr.": "Center",
            "Ctr,": "Center",
            "ctr": "Center",
            "ctr.": "Center",
            "ctr,": "Center",
            "Crt": "Court",
            "Crt.": "Court",
            "By-pass": "Bypass",
            "N.": "North",
            "N": "North",
            "E.": "East",
            "E": "East",
            "S.": "South",
            "S": "South",
            "W.": "West",
            "W": "West"
          }
          
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """
    Interate through the OSM file and return a dictionary containing street labels as keys
    and values of street names found with stated street labels.
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def update_name(name, mapping): # name is the actual string of the street, ex:  Keary st
    """(str, dict) -> str
    Check if ending chars of name contain an abbreviation, 
    if True, return updated name replacing abbreviation with matching value in mapping dictionary
    """
    n = street_type_re.search(name)  #this will check to see if there is an abbreviation at the end of name
    if n:  #if True, that is if there is indeed an identified abbreviation...
        street_type = n.group()  # here we will group or segment that abbreviation using group()
        if street_type in mapping: # if that abbreviation is found in our manual mapping
            name = name[:-len(street_type)] + mapping[street_type]  # it will swap it out here with the value in our dict mapping.
    return name

def update_names(audited_file):
    for street_type, ways in audited_file.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
