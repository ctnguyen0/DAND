def get_user(element):
    return


def process_map(filename):
    """
    Iterate through the OSM file in search for 'user' keys 
    and return a set containing a list of each unique user.
    Return the number of users in list.
    """
    users = set()
    for _, element in ET.iterparse(filename):
        key = 'user'
        if key in element.attrib:
            users.add(element.attrib['user'])
    print len(users), "users contributed to this dataset.  Thank you all!"
    return users
