import py360convert
import threading
import numpy as np
import cv2, os
from PIL import Image, ImageEnhance

equirect = cv2.imread('yuchuiyuan.jpg')
# newone = np.zeros_like(equirect)
# print(equirect.shape)
# equirect = cv2.resize(equirect, (8192, 3072))
# newone[512:4096-512, ...] = equirect
# equirect = newone

# equirect = equirect[512:4096-512, ...]
# equirect = cv2.resize(equirect, (8192, 4096))

os.makedirs('output', exist_ok=True)

fov_deg = 82
fps = 60
seconds = 30
frames = fps * seconds
threadCount = 8
threads = []
last = int(frames*(360-fov_deg/2) / 360)
part = int(last / threadCount)

def myThread(idx, part):
    for i in range(idx, idx+part):
        piece = py360convert.e2p(equirect, fov_deg=(fov_deg, fov_deg), u_deg=-135+i*(360/frames), v_deg=-10, out_hw=(1920, 1920), in_rot_deg=0, mode='bilinear')
        img = piece[420:1080+420, ...]

        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = ImageEnhance.Brightness(img)
        img = img.enhance(1.1)
        img = ImageEnhance.Contrast(img)
        img = img.enhance(1.1)
        
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

        cv2.imwrite(f'output/{i}.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 99])

for i in range(threadCount):
    idx = part*i
    if(i==threadCount-1):
        t = threading.Thread(target=myThread, args=(idx, last-idx))
    else:
        t = threading.Thread(target=myThread, args=(idx, part))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

# for i in range(idx+part, int(idx+part+part/2)):
#     scale = (i-idx-part)/5
#     piece = py360convert.e2p(equirect, fov_deg=(90-scale, 90-scale), u_deg=360*(idx+part)/3600, v_deg=-10, out_hw=(1920, 1920), in_rot_deg=0, mode='bilinear')
#     cv2.imwrite(f'piece4/{i}.png', piece[420:1500,...])

# piece = py360convert.e2p(equirect, fov_deg=(90, 90), u_deg=360*0/3600, v_deg=-10, out_hw=(1920, 1920), in_rot_deg=0, mode='bilinear')
# cv2.imwrite(f'piece4/0.jpg', piece)

# piece = py360convert.e2p(equirect, fov_deg=(60, 60), u_deg=-135, v_deg=0, out_hw=(1920, 1920), in_rot_deg=0, mode='bilinear')
# cv2.imwrite(f'piece4/1.jpg', piece[1920-1080:, ...])
