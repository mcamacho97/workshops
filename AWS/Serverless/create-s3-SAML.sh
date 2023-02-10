#create environment variables to use in aws cli
accountId=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .accountId)

s3_deploy_bucket="theme-park-sam-deploys-${accountId}"

echo $s3_deploy_bucket

#create bucket s3
aws s3 mb s3://$s3_deploy_bucket

#SAM
sam package --output-template-file packaged.yaml --s3-bucket $s3_deploy_bucket

sam deploy --template-file packaged.yaml --stack-name theme-park-ride-times --capabilities CAPABILITY_IAM

#SAM
sam build

sam package --output-template-file packaged.yaml --s3-bucket $s3_deploy_bucket

sam deploy --template-file packaged.yaml --stack-name theme-park-backend --capabilities CAPABILITY_IAM
