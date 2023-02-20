###Para crear diferentes perfilesde aws cli###
aws configure --profile account1
aws configure --profile account2

###Para descargar de un bucket s3 a otro bucket s3##
aws s3 cp --recursive s3://aws-dataengineering-day.workshop.aws/data/ s3://aws-labs-sistematica/Datos/tickets/ --profile sistematica

# Verify that your user is logged in by running the command aws sts get-caller-identity. Copy and paste the command into the Cloud9 terminal window.
aws sts get-caller-identity
