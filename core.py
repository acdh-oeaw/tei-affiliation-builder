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
for file in xml_dir_path.iterdir():

    # XML file level

    if file.is_file() and file.suffix == ".xml":

        # XML full tree level

        with open(file, "r") as xml_file:  # open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

            print(f"\nParsing {file}")  # printing will be replaced by logger
            root = etree.parse(xml_file)  # raises IOError if file nonexistent/unreadable; raise error.XMLSyntaxError if not well-formed

            # find events within listEvents

            event_list = root.xpath("//tei:listEvent/tei:event", namespaces=NS)  # target all events within all listEvents, all events are taken to be relevant

            if event_list:
                print(f"TEI event elements within listEvent detected: {event_list}")
            else:
                print("No TEI event elements within listEvent detected")

            # get to individual event

            for event in event_list:
                print("\n>>> single event:")
                print(event.tag, event.attrib, event.text)            

                # get to elements of individual event tree - this is a very unelegant and limited layered loop, to be replaced by recursion

                # for element in list(event):
                #     print("\n>>> single elements within single event:")
                #     print(element.tag, element.attrib, element.text)

                #     if list(element):
                #         for child1 in list(element):
                #             print("\n>>> single direct children of single elements within single events:")
                #             print(child1.tag, child1.attrib, child1.text)

                #             if list(child1):
                #                 for child2 in list(child1):
                #                     print("\n>>> single grandchildren of direct children of elements within events:")
                #                     print(child2.tag, child2.attrib, child2.text)

                #                 if list(child2):
                #                     for child3 in list(child2):
                #                         print("\n>>> single grandchildren of direct children of elements within events:")
                #                         print(child3.tag, child3.attrib, child3.text)   

                # try recursion instead

                def get_elements(layer):
                    if list(layer):
                        for element in list(layer):
                            print(element.tag, element.attrib, element.text)
                            if list(element):
                                get_elements(element)

                get_elements(event)


            print("\n#########")
        

    
