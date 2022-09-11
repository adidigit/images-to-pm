import argparse

import torch.utils.data
from torchvision.models import resnet18
parser = argparse.ArgumentParser()


parser.add_argument('--gpu', type=int, default=1, help='GPU to use [default: GPU 0]')
parser.add_argument('--batch', type=int, default=32, help='Batch Size during training [default: 32]')
parser.add_argument('--epoch', type=int, default=200, help='Epoch to run [default: 50]')
parser.add_argument('--output_dir', type=str, default='train_results', help='Directory that stores all training logs and trained models')
parser.add_argument('--wd', type=float, default=0, help='Weight Decay [Default: 0.0]')
FLAGS = parser.parse_args()
parser = argparse.ArgumentParser()
parser.add_argument("--dataset_path", type=str, default="data/UCF-101-frames", help="Path to UCF-101 dataset")
parser.add_argument("--split_path", type=str, default="data/ucfTrainTestlist", help="Path to train/test split")
parser.add_argument("--split_number", type=int, default=1, help="train/test split number. One of {1, 2, 3}")
parser.add_argument("--num_epochs", type=int, default=100, help="Number of training epochs")
parser.add_argument("--batch_size", type=int, default=16, help="Size of each training batch")
parser.add_argument("--sequence_length", type=int, default=40, help="Number of frames in each sequence")
parser.add_argument("--img_dim", type=int, default=224, help="Height / width dimension")
parser.add_argument("--channels", type=int, default=3, help="Number of image channels")
parser.add_argument("--latent_dim", type=int, default=512, help="Dimensionality of the latent representation")
parser.add_argument("--checkpoint_model", type=str, default="", help="Optional path to checkpoint model")
parser.add_argument(
    "--checkpoint_interval", type=int, default=5, help="Interval between saving model checkpoints"
)
opt = parser.parse_args()
print(opt)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train():

    device = TBD
    optimizer = TBD
    model = TBD
    model.to(device)

    dl = DataLoader
    for epoch in num_of_epochs:



if __name__ == '__main__':
    train()
