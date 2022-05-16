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
