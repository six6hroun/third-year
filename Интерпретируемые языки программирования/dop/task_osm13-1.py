import xml.etree.ElementTree as ET
OSM_FILE = "131.osm"
tree = ET.parse(OSM_FILE)
root = tree.getroot()

round_the_clock = set()
from_11_to_23 = set()
from_10_to_22 = set()

for element in root:
    if element.tag not in ("node", "way", "relation"):
        continue

    element_id = (element.tag, element.attrib.get("id"))

    for tag in element.findall("tag"):
        if tag.attrib.get("k") == "opening_hours":
            value = tag.attrib.get("v")
            if value == "24/7":
                round_the_clock.add(element_id)
            elif value == "11:00-23:00":
                from_11_to_23.add(element_id)
            elif value == "10:00-22:00":
                from_10_to_22.add(element_id)

print("Круглосуточно:", len(round_the_clock))
print("Количество объектов работающих с 11:00–23:00:", len(from_11_to_23))
print("Количество объектов работающих с 10:00–22:00:", len(from_10_to_22))