# Firebase Poetry GCP template

1. Create new project in GCP and set up firebase (with database)
2. Set up artifact registry, Cloud Run API
   1. Cloud Run API
      1. https://console.cloud.google.com/marketplace/product/google/run.googleapis.com
   2. Create repository in Artifact Registry
      1. https://console.cloud.google.com/artifacts/create-repo
      2. Name: prd-{project_name}
      3. Region: asia-northeast1 (Tokyo)
3. Create service account with the following permissions
   1. Cloud Deploy Runner
   2. Cloud Run Admin
   3. Artifact Registry Administrator
   4. Artifact Registry Service Agent
4. Set GCP_SA_KEY in github repository secret
5. Set project name and gcp project id
6. Commit and push the change to github
7. Set OPENAI_API_KEY in cloud run

make update-name
