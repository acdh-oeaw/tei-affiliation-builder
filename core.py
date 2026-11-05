# import libraries
# from collections import defaultdict  # for dictionary of events yet unknown
import json
from pathlib import Path  # for filepath operations

from lxml import etree  # for XML parsing

# some constants/variables
XML_DIR = "../../../Sandbox/some-xml-folder"  # this will be a build() parameter one day
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# create dictionary to hold event data, as temporary storage for event data
# event_dict = defaultdict(list)
event_dict = {}


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

            # recursive function to traverse XML tree from listEvent downward

            def build(target_dict, elements):  # pass currently to be filled (child-)dictionary; pass list of sibling LXML element objects to be processed
                for element in elements:

                    child_elements = list(element.iterchildren(tag=etree.Element))  # get list of direct child elements (only true elements); filter out comments

                    if element.tag == "{http://www.tei-c.org/ns/1.0}event":
                        try:
                            element_name = element.attrib["{http://www.w3.org/XML/1998/namespace}id"]  # replace non-unique element name with xml:id; i.e. require xml:id on event
                        except:  # catch KeyError
                            print("no xml:id on event element found")
                            continue
                    elif element.tag == "{http://www.tei-c.org/ns/1.0}person" or element.tag == "{http://www.tei-c.org/ns/1.0}org" or element.tag == "{http://www.tei-c.org/ns/1.0}object":
                        if element.attrib["sameAs"]:
                            try:
                                element_name = element.attrib["sameAs"]  # require @sameAs on relevant entities affiliated with events ...
                            except:
                                print("no sameAs on person/org/object element found")
                                continue
                        elif element.attrib["{http://www.w3.org/XML/1998/namespace}id"]:
                            try:
                                element_name = element.attrib["{http://www.w3.org/XML/1998/namespace}id"]  # and/or allow for @xml:id on relevant entities? (to be checked against TEI Guidelines)
                            except:
                                print("no xml:id on person/org/object element found")
                                continue
                    else:
                        element_name = element.tag

                    if child_elements or element.attrib:
             
                        nested_dict = {}

                        if element.attrib:

                            target_dict[element_name] = nested_dict
                            for attribute in element.attrib:
                                nested_dict[attribute] = element.attrib[attribute]  # populate nested dictionary with attributes; leave recursion if there are no child elements

                            if (not child_elements) and element.text:
                                nested_dict["content"] = element.text

                        if child_elements:

                            # open nested dictionary and pass into recursion to be populated at deeper level
                            target_dict[element_name] = nested_dict  # strictly speaking redundant; must remain in sync with same line further above
                            build(nested_dict, child_elements)

                    else:
                        target_dict[element_name] = element.text  # leave recursion for elements without attributes or child elements
                    





            build(event_dict, event_list)  # first call: pass top-level dictionary and listEvent
            print(json.dumps(event_dict, sort_keys=True, indent=4))  

                    
                        

                # else:
                    # event_id = event.tag

                # event_dict[event_id] = {}


                # if event.attrib:
                #     for attribute in event.attrib:
                #         print(f">>>>>> attributes of event element: {attribute}, {event.attrib[attribute]}")
                #         event_dict[event_id][attribute] = event.attrib[attribute]


            #    element_dict = {}

                # print("\n>>> single event:")
                # print(event.tag, event.attrib, event.text)

                # try:
                #     event_id = event.attrib["{http://www.w3.org/XML/1998/namespace}id"]  # catch KeyError 
                # except:
                #     print("no event id")
                #     continue
                # else:
                #     print(event_id)

                # event_dict[event_id] = element_dict

                # if event.attrib:
                #     for attribute in event.attrib:
                #         print(f"attributes of event element: {attribute}, {event.attrib[attribute]}")
                #         element_dict[attribute] = event.attrib[attribute]

                # if list(event):
                #     for element in list(event):

                #         print(f"elements: {element.tag}, {element.attrib}, {element.text}")

                #         if element.getparent().tag == "{http://www.tei-c.org/ns/1.0}event" and not len(element):
                #             event_dict[event_id][element.tag] = element.text
                #         elif element.getparent().tag == "{http://www.tei-c.org/ns/1.0}event" and len(element):
                #             event_dict[event_id][element.tag] = {}


                # event_dict.append()

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

            #         def get_elements(layer):
            #             # loop through elements within event node if there are any:
            #             if list(layer):
            #                 for x in list(layer):

            #                     print(f"elements: {x.tag}, {x.attrib}, {x.text}")




    
            #                     # loop through attributes of each element if there are any:
            #                     if x.attrib:
            #                         for attribute in x.attrib:
            #                             print(f"attribute: {attribute}, {x.attrib[attribute]}")

            #                     # recurse on elements within elements within event node if there are any:
            #                     if list(x):
            #                         get_elements(x)

            #         get_elements(element)


            # print("\n#########")


      

    
