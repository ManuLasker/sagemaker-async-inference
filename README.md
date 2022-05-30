# Sagemaker Async Inference

This repository contains Infrastructure as code (Cloudformation templates) to
deploy an asyncronous inference endpoint in sagemaker. The Idea is to make a
performance benchmark for this kind of endpoint.

## Underlying resources and infrastructure

The cloudformation templates deploy the following resources on AWS.

[x] S3 Bucket to upload and save the model artifact</br>
[x] Lambda to test sagemaker endpoint</br>
[x] Lambda Execution Role with the necessary permissions</br>
[x] Sagemaker Execution Role with the necessary permissions</br>
[x] Sagemaker Model</br>
[x] Sagemaker Endpoint Config</br>
[x] S3 Bucket to upload sagemaker endpoint's input and save sagemaker endpoint's results</br>
[x] Sagemaker Endpoint</br>
[x] Application Auto Scaling Target</br>
[x] Application Auto Scaling Policy</br>

## How to use this repository

There are three important folders in this repository and one bash script that we need to execute:

- *IaC folder*: this folder contains all the cloudformation templates to deploy our test previous describe infrastructure.</br>
- *call_sagemaker_lambda*: this folder contains code for a lambda function, this will be upload to a s3 bucket and then deployed to aws using the cloudformation templates.</br>
- *false_sagemaker_clients*: this folder contains a cli app that for this case it will create any number of concurrent clients to the call_sagemaker lambda function and it will also generate a csv file with differents kind of metadata for our experimentation, for example the status response for each request, the actual response, the time take for the request to complete, and so on.

### Execute experiments

To execute an experiment first, we need an AWS Account an credentials already configured, and a `.tar.gz` model artifact to be deployed on AWS Sagemaker this need to be save in the current direcorty, for this case it is not parametrized so it will be located in a folder name `./carta_labolar/firma/v2/model.tar.gz`, then we simply execute the script `deploy.sh` as follows:

```Bash
./deploy.sh no si
```

This will first deploy the mlops artifacts bucket and wait until completion, then it will upload the model artifact and the lambda `.zip` file, to finally deploy the main resources for the whole application. After the deployment's completion tu run one experiments, execute the following commands:

```Bash
cd false_sagemaker_clients
make init
make dev
conda activate ./env/
python run.py call-lambda -n 180
```

This will generate 180 concurrent invocation to the lambda function and wait, then after completion it will generate a `.csv` file with data to analyze our experiment.


## Results

The results of the experiments and benchmark for this kind of model is the following:

### 0 instances when the endpoint is not used (AutoScaling)

Thanks to the auto scaling configuration, when the endpoint is not in used it will scale in to 0 instances, thus it will not charge money and it will save costs:

![0_images](results/experiments/0_instancias.png)

### 150 calls to the endpoint

Current autoscaling configuration is up to two instances, with this configuration and having in account the 15 minutes timeout for the lambda function, the results were very good. The system was able to process 150 asynchronous request in 532 seconds (8.86 min), and thanks to the endpoint's internal queue the instances did not hang out.

![10_executions](results/experiments/lambda_execution/150_executions.png)

the cpu utilization of the system with two instances increase up to 119% and each instance process up to 4~7 request at a time.

[results_150_csv](false_sagemaker_clients/results/lambda_execution_05_22_2022_150.csv)

### 250 Calls to the endpoint

In this case, with current autoscaling and endpoint configurations, the results were good until it reached the 220 request call. Since the lambda function have a 15 minutes timeout, after the 220 processed requests, the rest 30 calls to the lambda function resulted in timeout exception. If we want to solve this problem I recommend increase the max instances parameter in the autoscaling configuration. So for 220 or more, I don't recommend the use with a lambda integration, because it will increase cost for the lambda function.

[results_250_csv](false_sagemaker_clients/results/lambda_execution_05_23_2022_250.csv)
