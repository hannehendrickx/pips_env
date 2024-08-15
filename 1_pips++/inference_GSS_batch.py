import time
import saverloader
from nets.pips2 import Pips
import utils.improc
from utils.basic import print_, print_stats
import torch
from tensorboardX import SummaryWriter
import torch.nn.functional as F
from fire import Fire
import sys
from pathlib import Path
import glob, os, cv2
import numpy as np

def run_model(model, rgbs, model_name, start_idx, S_max=128, N=64, iters=16):
    rgbs = rgbs.cuda().float()  # B, S, C, H, W

    B, S, C, H, W = rgbs.shape
    assert (B == 1)

    # pick N points to track; we'll use a uniform grid
    N_ = np.sqrt(N).round().astype(np.int32)
    grid_y, grid_x = utils.basic.meshgrid2d(B, N_, N_, stack=False, norm=False, device='cuda')
    grid_y = 8 + grid_y.reshape(B, -1) / float(N_ - 1) * (H - 16)
    grid_x = 8 + grid_x.reshape(B, -1) / float(N_ - 1) * (W - 16)
    xy0 = torch.stack([grid_x, grid_y], dim=-1)  # B, N_*N_, 2
    _, S, C, H, W = rgbs.shape

    # zero-vel init
    trajs_e = xy0.unsqueeze(1).repeat(1, S, 1, 1)

    iter_start_time = time.time()

    preds, preds_anim, _, _ = model(trajs_e, rgbs, iters=iters, feat_init=None, beautify=True)
    trajs_e = preds[-1]

    save_output_model(trajs_e, model_name, filenames[start_idx])

    iter_time = time.time() - iter_start_time
    print('inference time: %.2f seconds (%.1f fps)' % (iter_time, S / iter_time))

    return trajs_e

def save_output_model(trajs_e, model_name, original_filename):
    for i, layer in enumerate(trajs_e[0]):
        layer_np = layer.cpu().numpy()
        output_path = os.path.join('outputs', model_name)
        os.makedirs(output_path, exist_ok=True)

        # Extract the filename without extension
        base_filename = os.path.splitext(os.path.basename(original_filename))[0]

        # Create a unique name based on the original filename
        output_filename = f'{base_filename}_raw_points{i+1}.txt'
        np.savetxt(os.path.join(output_path, output_filename), layer_np)


def process_images_in_batches(model, rgbs, model_name, batch_size=10, S_max=128, N=64, iters=16):
    total_images = len(rgbs)

    for start_idx in range(0, total_images, batch_size):
        end_idx = start_idx + batch_size
        batch_rgbs = rgbs[start_idx:end_idx]

        batch_rgbs = torch.from_numpy(batch_rgbs).permute(0, 3, 1, 2).to(torch.float32)
        batch_rgbs = F.interpolate(batch_rgbs, image_size, mode='bilinear').unsqueeze(0)

        with torch.no_grad():
            trajs_e = run_model(model, batch_rgbs, model_name, start_idx, S_max=S_max, N=N, iters=iters)

        print(f"Processed images {start_idx + 1}-{end_idx} out of {total_images}")

    print("Processing complete")

S = 10  # seqlen change batch size in def process_images_in_batches
N = 1000  # number of points per clip
stride = 8  # spatial stride of the model
timestride = 1  # temporal stride of the model
iters = 16  # inference steps of the model
max_iters = 4  # number of clips to run
shuffle = False  # dataset shuffling
log_freq = 1  # how often to make image summaries
log_dir = './logs_demo'
init_dir = './reference_model'
device_ids = [0]

exp_name = 'de00'  # copy from dev repo

img_path = '/home/pips/PIPS/pips2/gss_images/Datasets paper/Cam4_Grabengufer22/1_Weekly no snow Stable sequence scaled 2021-2023'
filenames = glob.glob(os.path.join(img_path, '*.jpg'))
filenames = sorted(filenames)
name = "test_folder_name"

list_images = [cv2.imread(image) for image in filenames]
rgbs = np.array(list_images)
#rgbs = rgbs[:, :, :, ::-1].copy()  # BGR->RGB
rgbs = rgbs[::timestride]
S_here, H, W, C = rgbs.shape
image_size = rgbs.shape[1:3]
print('rgbs', rgbs.shape)

# autogen a name
model_name = "%s_%d_%d_%s" % (name, S, N, exp_name)
import datetime

model_date = datetime.datetime.now().strftime('%H%M%S')  #add hours, minutes and seconds to the ouputfolder name
model_name = model_name + '_' + model_date
print('model_name', model_name)

log_dir = 'logs_demo'
writer_t = SummaryWriter(log_dir + '/' + model_name + '/t', max_queue=10, flush_secs=60)

global_step = 0

model = Pips(stride=8).cuda()
parameters = list(model.parameters())
if init_dir:
    _ = saverloader.load(init_dir, model)
global_step = 0
model.eval()

idx = list(range(0, max(S_here - S, 1), S))
if max_iters:
    idx = idx[:max_iters]

process_images_in_batches(model, rgbs, model_name, S_max=S, N=N, iters=iters)
