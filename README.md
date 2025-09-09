# Alfred: The Chatbot

List out which model is available

```bash
aws bedrock list-foundation-models \
  --region us-west-1 \
  --output json | jq . > models.json
```

```bash
aws s3 cp knowledge_base.json s3://<BUCKET_NAME>/knowledge_base.json
```

https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-nova.html

https://docs.aws.amazon.com/nova/latest/userguide/using-invoke-api.html

https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html

https://docs.aws.amazon.com/nova/latest/userguide/complete-request-schema.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html
