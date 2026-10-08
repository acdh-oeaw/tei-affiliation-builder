# import libraries
from pathlib import Path  # for filepath operations
from lxml import etree  # for XML parsing


# some constants/variables
XML_DIR = "../../../Sandbox/some-xml-folder"  # this will be a build() parameter one day
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# transform and check XML directory path
xml_dir_path = Path(XML_DIR)
if not xml_dir_path.is_dir():
        raise FileNotFoundError

# loop through immediate children, but do not walk subdirectories recursively!
# so one requirement is this: one simple folder with XMLs (seems reasonable enough to me)
for entry in xml_dir_path.iterdir():

    # XML file level

    if entry.is_file() and entry.suffix == ".xml":

        print(entry)

        # XML full tree level

        root = etree.parse(entry)  # raise IOError if file nonexistent/unreadable; raise error.XMLSyntaxError if not well-formed

        # find events within listEvents

        event_list = root.xpath("//tei:listEvent/tei:event", namespaces=NS)  # target all events within all listEvents, all events are taken to be relevant
        print(event_list)

        # get to individual event tree level

        for event in event_list:
            print("---")
            print(etree.tostring(event))
            print("---")

            # get to elements of individual event tree

            for element in event.iter():
                print(element.tag, element.attrib, element.text)  # instead of printing, let's put this into a dict

        print("#########")
      

    
