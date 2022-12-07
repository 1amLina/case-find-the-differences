from PIL import Image
import os.path as osp
 
def glue_together(image1, image2, out_path):
    img1 = Image.open(image1) 
    img2 = Image.open(image2)
    width = img1.size[0]*2 #определяем ширину будущего "склеенного" изображения
    height = img1.size[1] #берем высоту первого изображения
    img = Image.new('RGB', (width, height))
    img.paste(img1, (0,0))
    img.paste(img2, (img1.size[0], 0))
    img.save(osp.join(out_path, 
                      f'{osp.basename(image1)}__{osp.basename(image2)}'))