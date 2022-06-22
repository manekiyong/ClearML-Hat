import os
import yaml
import argparse

from clearml import Task, Dataset

PROJECT_NAME = 'hat'

def config_to_list(train_args):
    args_list = []
    for x in train_args:
        # Handling Boolean Cases; ASSUMPTION: All boolean args are default store_true
        if type(train_args[x]) == bool and train_args[x] == False:
            continue
        if type(train_args[x]) == bool and train_args[x] == True:
            args_list.append('--'+x)
            continue
        args_list.append('--'+x)
        if type(train_args[x])==list:
            for k in train_args[x]:
                args_list.append(str(k))
        else: 
            args_list.append(str(train_args[x]))
    return args_list

if __name__ == '__main__':

    #ClearML Args
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_yaml', type=str, default='', help='path to yaml file of training configuration')
    parser.add_argument('--remote', action='store_true', help='Remote Execution')
    parser.add_argument('--s3', action='store_true', help='Retrieve Training Data from S3 instead')
    parser.add_argument('--task_name', type=str, default='task', help='ClearML Task Name')
    parser.add_argument('--data_proj_name', type=str, default='datasets/hat', help='dataset_project arg for ClearML Dataset')
    args = parser.parse_args()

    with open(args.train_yaml, 'r') as f:
        train_params = yaml.safe_load(f)
    
    Task.force_requirements_env_freeze(force=True, requirements_file='../requirements.txt')
    clearml_task = Task.init(project_name=PROJECT_NAME, task_name=args.task_name)
    clearml_task.connect(train_params, name='train_args')

    # Remote Execution
    if args.remote:
        clearml_task.set_base_docker("nvcr.io/nvidia/pytorch:21.09-py3")
        clearml_task.execute_remotely(queue_name='compute')
    
    # Data Retrieval
    if args.s3:
        # Retrieve data from S3
        dataset_path = Dataset.get(dataset_name='cat', dataset_project=args.data_proj_name).get_local_copy() # Get Train Data
        dataset_path = os.path.join(dataset_path, '')
        train_params['data_path'] = dataset_path #Overwrite with clearml cached path
    else:
        # Retrieve data locally
        train_params['data_path'] = './data/Images/'

    import train_aip
    args_list = config_to_list(train_params)
    print(args_list)
    train_aip.main(args_list)