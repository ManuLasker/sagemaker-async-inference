# Sagemaker Async Inference

This repository contains Infrastructure as code (Cloudformation templates) to 
deploy an asyncronous inference endpoint in sagemaker. The Idea is to make a 
performance benchmark for this kind of endpoint.

## Underlying resources and infrastructure

The cloudformation templates deploy the following resources on AWS.

[x] S3 Bucket to upload and save the model artifact
[x] Sagemaker Model
[x] Sagemaker Endpoint Config
[x] S3 Bucket to upload sagemaker endpoint's input and save sagemaker endpoint's results
[x] Sagemaker Endpoint
[x] Application Auto Scaling Target
[x] Application Auto Scaling Policy
