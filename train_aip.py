import argparse
import time
from PIL import Image
from tqdm import tqdm

def train():
    for j in tqdm(range(100)):
        time.sleep(0.01)

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=3)
    parser.add_argument('--model_name', type=str, default='some_model')
    parser.add_argument('--data_path', type=str, default='data/Images/')
    parser.add_argument('--img_size', nargs='+', type=int, default=[640, 640])
    parser.add_argument('--augment', action='store_true')
    opt = parser.parse_args(args)
    print(vars(opt))
    for i in range(opt.epochs):
        print("Epoch {}/{}".format(i+1, opt.epochs))
        train()
    im = Image.open(opt.data_path+'cat1.jpg')
    im.show()

if __name__ == '__main__':
    main()
