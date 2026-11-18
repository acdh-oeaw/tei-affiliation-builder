# imports
import pprint  # for data pretty printing
from pathlib import Path  # for filepath operations

from lxml import etree  # for XML parsing

# constants
XML_DIR = "../../../Sandbox/some-xml-folder"  # DEV: will be build() param; REQUIREMENT: one flat folder (non-exclusively) containing XMLs
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# check XML directory path
xml_dir_path = Path(XML_DIR)

if xml_dir_path.is_dir():
    print(f"{xml_dir_path.resolve()} found")  # DEV: log
else:
    raise FileNotFoundError(f"Filepath {xml_dir_path} is invalid, inaccessible, missing, or points to something other than a directory") # https://docs.python.org/3/library/pathlib.html#pathlib.Path.is_dir

# create dictionary as temporary storage for event data
event_dict = {}

# loop through XML files
for file in xml_dir_path.iterdir(): # https://docs.python.org/3/library/pathlib.html#pathlib.Path.iterdir

    if file.is_file() and file.suffix == ".xml":

        # XML full tree level

        with open(file, "r") as xml_file:  # open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

            print(f"\nParsing {file}")  # printing will be replaced by logger
            root = etree.parse(xml_file)  # raises IOError if file nonexistent/unreadable; raise error.XMLSyntaxError if not well-formed
    elif not file.is_file:
        raise FileNotFoundError(f"File {file}")
    elif file.suffix != ".xml":
        print("not an XML")

    # find events within listEvents

    event_list = root.xpath("//tei:listEvent/tei:event", namespaces=NS)  # target all events within all listEvents, all events are taken to be relevant

    if event_list:
        print(f"TEI event elements within listEvent detected: {event_list}")
    else:
        print("No TEI event elements within listEvent detected")

    # recursive function to traverse XML tree from listEvent downward

    def build_dict(target_dict, elements):  # pass currently to be filled (child-)dictionary; pass list of sibling LXML element objects to be processed

        # list and iterator for handling multiple elements with same tags
        tags_list = []
        i = 0

        # pre-loop: create list of element tags for handling multiple identical tag names in main loop
        for element in elements:

            tags_list.append(element.tag)
        
        for element in elements:

            child_elements = list(element.iterchildren(tag=etree.Element))  # get list of direct child elements (only true elements); filter out comments

            if element.tag == "{http://www.tei-c.org/ns/1.0}event":
                try:
                    element_name = element.attrib["{http://www.w3.org/XML/1998/namespace}id"]  # replace non-unique element name with xml:id; i.e. require xml:id on event
                except:  # catch KeyError
                    print(f"no xml:id on event element {element} found")
                    continue
            
            elif element.tag == "{http://www.tei-c.org/ns/1.0}person" or element.tag == "{http://www.tei-c.org/ns/1.0}org" or element.tag == "{http://www.tei-c.org/ns/1.0}object":
                try:
                    element_name = element.attrib["sameAs"]
                except:  # catch KeyError
                    print(f"no sameAs on event element {element} found")
                    continue
                
            elif tags_list.count(element.tag) > 1:
                i += 1
                element_name = f"{element.tag}-{i}"

            else:
                element_name = element.tag

            if child_elements or element.attrib:
        
                nested_dict = {}

                if element.attrib:

                    target_dict[element_name] = nested_dict
                    for attribute in element.attrib:
                        nested_dict[attribute] = element.attrib[attribute]  # populate nested dictionary with attributes; leave recursion if there are no child elements

                    if (not child_elements) and element.text:
                        nested_dict["element-content"] = element.text

                if child_elements:

                    # open nested dictionary and pass into recursion to be populated at deeper level
                    target_dict[element_name] = nested_dict  # strictly speaking redundant; must remain in sync with same line further above
                    build_dict(nested_dict, child_elements)

            else:
                target_dict[element_name] = element.text  # leave recursion for elements without attributes or child elements


    build_dict(event_dict, event_list)  # first call: pass top-level dictionary and listEvent
            

pprint.pp(event_dict, width=150, expand=True, sort_dicts=True)  # expand param requires Python 3.15
