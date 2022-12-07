import xml.etree.ElementTree as ET
from tqdm import tqdm
import os.path as osp
from PIL import Image

def new_glue_together(image1, image2, out_path):
    img1 = Image.open(image1)
    img2 = Image.open(image2)
    
    width = img1.size[0]*2+int(img1.size[0]/80)
    height = img1.size[1]

    img = Image.new('RGB', (width, img1.size[1]))
    img.paste(img1, (0,0))
    img.paste(img2, (img1.size[0]+int(img1.size[0]/80), 0))
    img.save(osp.join(out_path, f'{osp.basename(image1)}__{osp.basename(image2)}'))

def new_make_patches(w_start, h_start, ROWS_PER_IMAGE = 10):
    coords = []
    frame_w = w_start//2-int((w_start//2)*0.005964)
    
    side = h_start//ROWS_PER_IMAGE
    x, y, w, h = (0, 0, side, side)
    while y < h_start:
        x = 0
        while x < frame_w:
            w_ = min(w, frame_w - x)
            h_ = min(h, h_start - y)
            coords.append([
                (x+w_,y), 
                (x+w_,y+h_), 
                (x,y+h_), 
                (x,y),
                (x+w_ + frame_w + int(frame_w/80), y), 
                (x+w_ + frame_w + int(frame_w/80), y+h_), 
                (x + frame_w + int(frame_w/80), y+h_), 
                (x + frame_w + int(frame_w/80), y)
            ])
            x += w
        y += h
    return coords                                    

def pre_annotation(empty_annotation, pre_annotation):

    tree = ET.parse(empty_annotation)
    root = tree.getroot()
    for child in tqdm(root):
        if child.tag not in {'version', 'meta'}:
            image_coords = new_make_patches(int(child.attrib['width']), 
                                            int(child.attrib['height']), 10)
            
            for coord in image_coords:
                str_coords = ""
                for c in coord:
                    if c != coord[-1]:
                        str_coords += str(c[0])+', '+str(c[1])+'; '
                    else:
                        str_coords += str(c[0])+', '+str(c[1])
                bbox = ET.Element('polygon', label="без изменений", occluded="0", 
                                  source="pre_annotated", points=str_coords, 
                                  z_order="0")
                child.append(bbox)

    xml_str = ET.tostring(root, encoding='utf-8', method='xml')

    with open(osp.join(pre_annotation,'pre_annotation.xml'), 'wb') as xmlfile:
        xmlfile.write(xml_str)
        xmlfile.close()  