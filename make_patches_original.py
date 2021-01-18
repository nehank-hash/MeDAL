import openslide
import numpy as np
import PIL
from PIL import Image
import os

def check_white_2(patch, w_threshold, size):
    num0 = np.sum(patch[:,:,0] < w_threshold)
    num1 = np.sum(patch[:,:,1] < w_threshold)
    num2 = np.sum(patch[:,:,2] < w_threshold)
    if(num0 > (size*size/2) or num1 > (size*size/2) or num2 > (size*size/2)):
        return True
    return False

svs_files = [s[:-1] for s in open('/home/satpura/Desktop/good_adeno_svs')]
save_dir = '/home/Drive2/NIT_patches/adeno'
# svs_files = ['/home/Drive2/DATA_LUNG_TCGA/data_squamous/78fae015-41a7-443f-90d4-7b4556cfeaa5/TCGA-22-0940-01A-01-TS1.e6789daf-32c1-4937-a0fc-b307fc728286.svs']

window = 1536*4
slide = 1536

tto_cnt = 0
svs_cnt = 0
# for svs in svs_files:
for i in range(42, len(svs_files)):
	svs = svs_files[i]
	# print svs
	svs_cnt += 1
	print(svs_cnt)
	# save_dir = svs.split('/')[-1][:-4]
	# save_dir = os.path.join('/home/Drive2/adeno_patches/', save_dir)
	
	# print save_dir
	image = openslide.OpenSlide(svs)
	fname = svs.split('/')[-1][:-4].split('.')[0]
	# print('======')
	print(fname)
	# print('======')
	w, h = image.dimensions
	cnt = 0
	for x in range(0, w - window, window):
		for y in range(0, h - window, window):
			patch = image.read_region((x, y), 1, (slide, slide))
			check = np.asarray(patch)[:,:,:3]
			if check_white_2(check, 200, slide):
				cnt += 1
				patch.save(os.path.join(save_dir, fname + '__' + str(x)+'__'+str(y)+'.png'))
	print cnt
	tto_cnt += cnt

print tto_cnt