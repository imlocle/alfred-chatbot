# Alfred: The Chatbot

An AI chatbot using AWS Bedrock and Python that answers questions about Loc.

## Technologies

- [AWS Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html)
- [AWS Nova Lite](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html)
- S3
- Terraform
- Python

## Dependencies

- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

## Listing Your Models

List out which model is available

```bash
aws bedrock list-foundation-models \
  --region <AWS_REGION> \
  --output json | jq . > models.json
```

## Add Knowledge Base into S3 Bucket

```bash
aws s3 cp knowledge_base.json s3://<BUCKET_NAME>/knowledge_base.json
```

Example of `knowledge_base.json`

```json
{
  "personal_info": {
    "first_name": "Loc",
    "last_name": "Le",
    "role": "Backend Cloud Engineer",
    "experience": "",
    "location": "Earth",
    "skills": []
  },
  "projects": [],
  "contact_info": {},
  "fun_facts": [],
  "hobbies": []
}
```

## Deployment

```bash
make clean && make deploy ENV=dev
```

## Resources

- [AWS Bedrock: InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
- [AWS Nova: Using Invoke API](https://docs.aws.amazon.com/nova/latest/userguide/using-invoke-api.html)
- [AWS Nova: Request Schema](https://docs.aws.amazon.com/nova/latest/userguide/complete-request-schema.html)
