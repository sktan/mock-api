# Serverless Mock API

This is a very simple serverless AWS application that runs on AWS gateway.
It's designed as a mock API service, speeding up the development / testing of your web applications without relying on the completion of backend APIs.

# Requirements

The following services and tools are used to run our mock API service.

- [Serverless](https://www.serverless.com/framework/docs/getting-started/)
- [An AWS Account](https://aws.amazon.com/)
- A valid domain from any provider
- [A valid ACM Certificate](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)

Create the ACM certificate in the region you are deploying in (in my case, ap-southeast-2).

# Deployment

The entire API serice can be deployed via CLI by following the instructions below.

## Pre-Requisites

Create a copy of `.env_example` named as `.env` and replace the variables.

## Deployment

Deploy the API into your AWS account
```
source .env
cd mock-api
sls deploy --region ap-southeast-2
```

Grab the `MockApiDomain` output value from Cloudformation, and then create CNAME entries under your domain. This can be done as either `*.api.example.com` or `test.api.example.com` + `test2.api.example.com`. The output can be grabbed by using the AWS cli command below (replacing mock-api-dev if you have replaced this with custom stack name).

```
aws cloudformation describe-stacks --stack-name "mock-api-dev" --region ap-southeast-2 --query "Stacks[0].Outputs[*].{Key: OutputKey, Value: OutputValue}" --output table
```

# Configuring Data

A DynamoDB table will be created, where you can craft HTTP responses based on the following fields:

| Column   | Type    | Description                                  |
|----------|---------|----------------------------------------------|
| Hostname | String  | The HTTP host your API will respond on       |
| Path     | String  | The HTTP URL your API will respond on        |
| Auth     | Boolean | Whether the Authorization header is required |
| Data     | Map     | A JSON object with data to respond with      |

Insert rows into your table and start hitting the API paths you have setup.

# Requesting Data

You will now be able to send HTTP requests to your configured URIs.
For troubleshooting purposes, the API will return the hostname and path you hit upon failure:

```
[sktan@devbox ~]$ curl -s https://test.api.example.com/test | jq
{
  "Errors": [
    "page not found"
  ],
  "Path": "/test",
  "Hostname": "test.api.example.com"
}
```
