# ClearML Hat

The motivation behind this repository is that i'm a lazy man and do not like to make a ton of edit on existing ML `train.py` scripts. Riding on the fact that most ML training scripts are executed by `python train.py --args1 val1 --args2 val2`, this repository aims to:
1) Make minimal edit on the original `train.py`
2) Decouple ClearML bits from `train.py` script, allowing the script to still be executable as a standalone script
3) Achieve the above without any additional Python packages

Kinda like just putting a hat over your train script

### Pre-requisites: 
* ClearML config (`clearml.conf`) with s3 keys

### Key Assumption:
* For boolean arguments in `train.py`, they are all `store_true`.

## 1. Environment setup
* First and foremost, create a Github Repository for the project.  Note that the repository **must** be public. I don't set the rules
* Next, have a virtual environment set up on your local machine (either Python venv or conda env is fine).
* Next, install the necessary dependencies for the project with the following amendments to `requirements.txt`:
    * Include the necessary packages indicated in the `requirements.txt` of this repository. 
    * Comment out `torch` and `torchvision` if you intend to use the PyTorch docker image (recommended) for remote execution. The PyTorch docker image already has these packages installed for you. If you intend to execute locally, and use ClearML solely for tracking purpose, then you may leave these two dependencies in.

## 2. Convert `train.py` argparse arguments to a `.yaml` file
Instead of typing a long list of args each time you run a new experiment, it is a good practice to store your experiment parameters as a `.yaml` file. This step will generate a `.yaml` file based on the default parameters from your `train.py`.  
* From your original `train.py` script, copy the `add_argument()` lines over to `argparse_to_yaml.py` and replace line 8-12. 
* Execute `python argparse_to_yaml.py` to generate a default `config.yaml`. 

## 3. Modification to `train.py` script
* Firstly, define a new function `main(args=None)` in your `train.py` (Refer to line 10 in `train_aip.py`).
* Next, copy everything in the main routine of `train.py` into `main()` function (Refer to line 11-23 in `train_aip.py`).
* Add `args` as the parameter for `parser.parse_args()` (Refer to line 17 in `train_aip.py`)
* Lastly, replace the main routine with `main()` function call (Refer to line 26 in `train_aip.py`)

You may compare `train_ori.py` and `train_aip.py` to see the changes applied. Despite the amendments, `train_aip.py` can still be executed in the same manner as `train_ori.py` (e.g. `python train_aip.py --epochs 2`)

## 4. Upload Training Data to S3 (For remote execution)
* In the `data` folder, edit the `S3_LINK` in `upload_dataset_to_s3.py` (Courtesy of Nic) to point to the s3 bucket (Line 3)
* Edit the dataset project and the dataset name (e.g. train/val/test) as well (Line 5). The convention for dataset project is `datasets/<project_name>`.
* Lastly, edit the path to your dataset (Line 6)

## 5. Putting on the ClearML Hat
The `hat.py` script handles most of the ClearML bits. This script initialize the ClearML task, setup for remote execution, and retrieves data from s3. 
1. On Line 7, change the `PROJECT_NAME`. 
2. On Line 46, change the base docker image, if necessary. You may also add other docker setup scripts here using the `docker_setup_bash_script` parameter. Refer to [ClearML Task Documentation](https://clear.ml/docs/latest/docs/references/sdk/task/#set_base_docker) for more details 
3. On Line 47, indicate your queue name, if necessary. 
4. On Line 52, modify the `dataset_name` to your respective dataset. The `get_local_copy()` method downloads and cache the data, then returns the path of the cache folder. This is why the dataset path needs to be overwritten on Line 54. 
5. On Line 59, the `train_aip.py` script will then be imported. This is because in the case of remote execution, prior to Line 46-47, all other Python packages would not have been ready, thus, importing the `train_aip.py` at the top of the script will yield error. (Shearman say one) 
6. On Line 60, the training parameters from the `.yaml` file will be converted in a list (e.g. `['--data_path', './data/Images', '--epochs', '10', '--img_size', '640', '640', '--model_name', 'some_model']`). This list can then be passed to the `train_aip.py` script, in Line 62. 

## 6. Commit changes to Github
yeah, commit your changes. otherwise it doesn't work sometimes. i honestly don't know why

## 7. Run Experiment!
* Local execution, local file path: `python hat.py --train_yaml config.yaml --task_name local`
* Local execution, s3 file path: `python hat.py --train_yaml config.yaml --task_name local_s3 --s3`
* Remote execution, s3 file path: `python hat.py --train_yaml config.yaml --task_name local_s3 --s3 --remote`

## 8. Cloning & Re-running experiments
On ClearML, you can repeat the experiments with minor tweaks to the parameter if the experiment is executed remotely. 
1) On the experiment page, right click on a complete task, then click on Clone
2) Give the task a name, then proceed to clone. 
3) The cloned experiment will be in the Draft state. Click on the task, and under the Configuration tab, you can edit the hyperparameters. (Note: The hyperparameters to be amended is under `train_args` **NOT** `Args`. The hyperparameters under `Args` are the defaults)
4) Once done, right click on the draft task and enqueue it onto one of the queues.


## Quirks to be fixed:
* To remove the default hyperparameters shown under `Args`