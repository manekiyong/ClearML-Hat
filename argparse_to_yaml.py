import argparse
import yaml


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    # REPLACE WITH YOUR ARGS BELOW
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--model_name', type=str, default='some_model')
    parser.add_argument('--data_path', type=str, default='data/Images/')
    parser.add_argument('--img_size', nargs='+', type=int, default=[640, 640])
    parser.add_argument('--augment', action='store_true')
    # REPLACE WITH YOUR ARGS ABOVE
    args = parser.parse_args()
    with open('config.yaml', 'w') as yaml_file:
        yaml.dump(vars(args), yaml_file, default_flow_style=False)
