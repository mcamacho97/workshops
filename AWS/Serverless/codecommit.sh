# This commands help to use the credentials of cloud9 to connect code commit
git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true


# Push the downloaded code to populate your recently created CodeCommit repository:
AWS_REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/\(.*\)[a-z]/\1/')
git push --set-upstream https://git-codecommit.$AWS_REGION.amazonaws.com/v1/repos/theme-park-frontend main

