def audit_zipcode(invalid_zipcodes, zipcode):
    twoDigits = zipcode[0:2]
    
    if twoDigits != 94 or not twoDigits.isdigit():
        invalid_zipcodes[twoDigits].add(zipcode)
        
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zip(osmfile):
    osm_file = open(osmfile, "r")
    invalid_zipcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    audit_zipcode(invalid_zipcodes,tag.attrib['v'])

    return invalid_zipcodes

audited_zipcode_sf = audit_zip(OSMFILE)


def update_zip(zipcode):
    """(str) -> str
    Return 5 digit zipcodes.
    """
    zipChar = re.findall('[a-zA-Z]*', zipcode)
    if zipChar:
        zipChar = zipChar[0]
    zipChar.strip()
    if zipChar == "CA":
        updateZip = re.findall(r'\d+', zipcode)
        if updateZip:
            return (re.findall(r'\d+', zipcode))[0]
    else:
        return (re.findall(r'\d+', zipcode))[0]

def update_zips(datafile):
    for street_type, ways in sf_zipcode.iteritems():
        for name in ways:
            better_name = update_zip(name)
            print name, "=>", better_name
