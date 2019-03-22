
# coding: utf-8

# In[15]:


"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "C:\Users\Vijin\Udacity\Part 4\Project\Palm Beach County.osm"

#Regular expression to get the street type
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# This is the mapping dictionary which illustrates what Street Types need to be fixed
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "Blvd.": "Boulevard",   
           "Blvd": "Boulevard",
           "Dr": "Drive",
           "Dr.": "Drive"
            }

#Filtering street types. All the inconsistent street types are filtered out
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
            
# Filtering postcodes. Postcodes starting with 334 are only considered valid            
def audit_post_code(postcode_types, postcode):
    if postcode.startswith("334"):
        postcode_types['valid'].add(postcode)
    else:
        postcode_types['invalid'].add(postcode)
        
        
# Filtering phone numbers. Phone numbers in xxx-xxx-xxxx are only considered valid     
def audit_phone(phone_types, phone):
    matchtel=re.match(r'\d{3}-\d{3}-\d{4}',phone)
    if matchtel:
        phone_types['valid'].add(phone)
    else:
        phone_types['invalid'].add(phone)        


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def is_phone(elem):
    return (elem.attrib['k'] == "phone")


def auditStreet(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
# Correct street type
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
            
    osm_file.close()
    return street_types

def auditPostCode(osmfile):
    osm_file = open(osmfile, "r")
    postcode_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
            
# Correct Post Code
                if is_postcode(tag):
                    audit_post_code(postcode_types, tag.attrib['v'])
    osm_file.close()
    return postcode_types

def auditPhone(osmfile):
    osm_file = open(osmfile, "r")
    phone_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
            
# Correct Telephone
                if is_phone(tag):
                    audit_phone(phone_types, tag.attrib['v'])
    osm_file.close()
    return phone_types


def update_name(name, mapping):

    # Updating Inconsistent street types
    for key,value in mapping.items():
        #print 'Name, Key and Value is ', name," " , key, " ", value
        updatedName=name
        if key in name:
            updatedName=re.sub(key,value,name)
            print 'Updated Name is: ',updatedName
            break

    return updatedName

def update_postcode(pcodetypes):

    # Update Post code which starts with FL
    updatedPostCodeList=[]
    for key,value in pcodetypes.items():
        print 'Key and Value is ', key, " ", value
        if key == 'invalid':
            for item in iter(value):
                if item.startswith('FL'):
                    print 'Post code before update is ', item
                    updatedPostCode=re.sub('FL','',item)
                    updatedPostCode.replace(' ','')
                    updatedPostCodeList.append(updatedPostCode)
                    print 'Updated post code is ', updatedPostCode

    return updatedPostCodeList

def update_phone(phonetypes):
    
    #Update phone numbers in the following formats +1 xxx-xxx-xxxx, +1-xxx-xxx-xxxx, +1 (xxx)-xxx-xxxx to xxx-xxx-xxxx
    #Update phone numbers in the following format (xxx)-xxx-xxxx, (xxx) xxx-xxxx to xxx-xxx-xxxx
    updatedPhoneList=[]
    for key,value in phonetypes.items():
        if key == 'invalid':
            for item in iter(value):
                if item.startswith('+1'):
                    print 'Phone number before update is ', item
                    updatedPhone=re.sub(r'^(\+1\D?)','',item)
                    updatedPhone1=re.sub(r'[\(\)]','',updatedPhone)
                    updatedPhone2=re.sub(r'\s','-',updatedPhone1)
                    updatedPhoneList.append(updatedPhone2)
                    print 'Updated phone number is ', updatedPhone2
                
                elif item.startswith('('):
                    print 'Phone number before update is ', item
                    updatedPhone=re.sub(r'[\(\)]','',item)
                    updatedPhone1=re.sub(r'\s','-',updatedPhone)
                    updatedPhoneList.append(updatedPhone1)
                    print 'Updated phone number is ', updatedPhone1

    return updatedPhoneList
    

def test():
    st_types = auditStreet(OSMFILE)
    pcode_types=auditPostCode(OSMFILE)
    phone_types=auditPhone(OSMFILE)
   
    pprint.pprint(dict(pcode_types))
    pprint.pprint(dict(phone_types))
    update_postcode(pcode_types)
    update_phone(phone_types)

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            

if __name__ == '__main__':
    test()


# In[ ]:




