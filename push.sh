docker build -t nigel-temp-repository .

aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 352369962800.dkr.ecr.ap-southeast-2.amazonaws.com

docker tag nigel-temp-repository:latest 352369962800.dkr.ecr.ap-southeast-2.amazonaws.com/nigel-temp-repository:latest

docker push 352369962800.dkr.ecr.ap-southeast-2.amazonaws.com/nigel-temp-repository:latest
