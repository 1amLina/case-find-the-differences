import xml.etree.ElementTree as ET
from tqdm import tqdm
import os.path as osp

def make_patches(w, h, numb_lines=10): #создание списка координат bbox'a
    step = int(h / numb_lines)
    coords = []
    
    for x in range(0, w, step):
        for y in range(0, h, step):
            x1, y1, x2, y2 = x, y, x + step, y + step
            coords.append((x1, y1, x2, y2))
    return coords

  
def pre_annotation(empty_annotation, pre_annotation):
		#создание нового файла разметки
    tree = ET.parse(empty_annotation)
    root = tree.getroot()
    for child in tqdm(root):
        if child.tag not in {'version', 'meta'}:
            image_coords = make_patches(int(child.attrib['width']), 
                                        int(child.attrib['height']), 10)
            
            for coord in image_coords:
                bbox = ET.Element('box', label="без изменений", occluded="0", 
                                  source="pre_annotated", 
                                  xtl=str(coord[0]),  ytl=str(coord[1]), 
                                  xbr=str(coord[2]), 
                                  ybr=str(coord[3]),z_order="0")
                child.append(bbox)

    xml_str = ET.tostring(root, encoding='utf-8', method='xml')

    with open(osp.join(pre_annotation,'pre_annotation.xml'), 'wb') as xmlfile:
        xmlfile.write(xml_str)
        xmlfile.close() 