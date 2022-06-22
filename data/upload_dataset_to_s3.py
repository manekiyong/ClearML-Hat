from clearml import Dataset

S3_LINK=''

dataset = Dataset.create(dataset_name='cat', dataset_project = 'datasets/hat')
dataset.add_files('./Images/')
dataset.upload(output_url=S3_LINK)
dataset.finalize()