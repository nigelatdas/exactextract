---
runme:
  id: 01HHDHAQJG9J2N5JKSW520ZA5B
  version: v2.0
---

###Todays Backlog 

* Run image as a task and generate data

- [ ] Run EE reading data from s3
- [ ] Write to s3
- [ ] Write to Mongo
- [x] Republish Docker Image
- [ ] Permissions to read bucket s3
- [x] VPC? ETL default
- [x] Security Groups? ETL nigels-temp-sg
- [ ] Task Role
- [ ] Execution Role
- [ ] VPC Endpoint to access ECR.Api
- [ ] 

 
Task Failure Reason Analysis:
#############################

REGISTRY CHECKS
===============
The registry domain [352369962800.dkr.ecr.ap-southeast-2.amazonaws.com] encountered socket connection failure for DNS Resolved IP(s) ['10.0.66.95', '10.0.66.95', '10.0.66.95', '10.0.7.74', '10.0.7.74', '10.0.7.74', '10.0.36.57', '10.0.36.57', '10.0.36.57'] with same network settings used by ECS / Fargate Agent. For more information check the following Knowledge Center articles:
- https://aws.amazon.com/premiumsupport/knowledge-center/ecs-pull-container-api-error-ecr/ 
- https://aws.amazon.com/premiumsupport/knowledge-center/ecs-pull-container-error/ 

The IP's [['10.0.66.95', '10.0.66.95', '10.0.66.95', '10.0.7.74', '10.0.7.74', '10.0.7.74', '10.0.36.57', '10.0.36.57', '10.0.36.57']] resolved from domain name [352369962800.dkr.ecr.ap-southeast-2.amazonaws.com] is not allowed in the egress of Security Group/s [['sg-006853aeb4afa1d57']] that is used by ECS/Fargate Agent

You have enabled ECR related private endpoints ['ecr.dkr', 'ecr.api'], However missing endpoint/s {'s3'} 
See https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html 

The route table rtb-024016eb9382fa95d associated with Task Subnet subnet-0db9ab8b465a54896 does not have network access either via Internet Gateway or Nat Gateway.
If you are leveraging custom networking path via peered network or via Transit Gateway please ensure the subnet where the task is placed have network connectivity to pull all required resources

VPC Endpoint (ecr.dkr) Security Group (sg-006853aeb4afa1d57) is not allowing the Inbound traffic.
 The Security Group associated with the VPC Endpoint should allow the traffic from Fargate Task/EC2 Instance Security Group on port 443 TCP.
For more information on the VPC endpoints prerequisites, refer the below documentationhttps://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html

[ecr.dkr VPC Endpoint]: Security Group rules for ['sg-006853aeb4afa1d57'] are not allowing the egress traffic.
Task ENI incase of Fargate or Container instance primary network interface incase of EC2 Launch type need egress access to communicate with external endpoint such as container registry, logging destination to spin upthe task If you are using either public subnet or private subnet with NAT GW, the rule should allow the Outbound traffic for protocol TCP on port 443 and destination 0.0.0.0/0.
See https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_instances.html#container_instance_concepts

VPC Endpoint (ecr.api) Security Group (sg-006853aeb4afa1d57) is not allowing the Inbound traffic.
 The Security Group associated with the VPC Endpoint should allow the traffic from Fargate Task/EC2 Instance Security Group on port 443 TCP.
For more information on the VPC endpoints prerequisites, refer the below documentationhttps://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html

[ecr.api VPC Endpoint]: Security Group rules for ['sg-006853aeb4afa1d57'] are not allowing the egress traffic.
Task ENI incase of Fargate or Container instance primary network interface incase of EC2 Launch type need egress access to communicate with external endpoint such as container registry, logging destination to spin upthe task If you are using either public subnet or private subnet with NAT GW, the rule should allow the Outbound traffic for protocol TCP on port 443 and destination 0.0.0.0/0.
See https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_instances.html#container_instance_concepts

The route table rtb-024016eb9382fa95d associated with Task Subnet subnet-0db9ab8b465a54896 does not have network access either via Internet Gateway or Nat Gateway.
If you are leveraging custom networking path via peered network or via Transit Gateway please ensure the subnet where the task is placed have network connectivity to pull all required resources


Log Configuration Checks
========================
The registry domain [logs.ap-southeast-2.amazonaws.com] encountered socket connection failure for DNS Resolved IP(s) ['10.0.61.209', '10.0.61.209', '10.0.61.209', '10.0.67.58', '10.0.67.58', '10.0.67.58', '10.0.5.153', '10.0.5.153', '10.0.5.153'] with same network settings used by ECS / Fargate Agent. For more information check the following Knowledge Center articles:- https://aws.amazon.com/premiumsupport/knowledge-center/ecs-pull-container-api-error-ecr/ 
- https://aws.amazon.com/premiumsupport/knowledge-center/ecs-pull-container-error/ 

The IP's [['10.0.61.209', '10.0.61.209', '10.0.61.209', '10.0.67.58', '10.0.67.58', '10.0.67.58', '10.0.5.153', '10.0.5.153', '10.0.5.153']] resolved from domain name [logs.ap-southeast-2.amazonaws.com] is not allowed in the egress of Security Group/s [['sg-006853aeb4afa1d57']] that is used by ECS/Fargate Agent

VPC Endpoint (logs) Security Group (sg-006853aeb4afa1d57) is not allowing the Inbound traffic.
 The Security Group associated with the VPC Endpoint should allow the traffic from Fargate Task/EC2 Instance Security Group on port 443 TCP.
For more information on the VPC endpoints prerequisites, refer the below documentationhttps://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html

[logs VPC Endpoint]: Security Group rules for ['sg-006853aeb4afa1d57'] are not allowing the egress traffic.
Task ENI incase of Fargate or Container instance primary network interface incase of EC2 Launch type need egress access to communicate with external endpoint such as container registry, logging destination to spin upthe task If you are using either public subnet or private subnet with NAT GW, the rule should allow the Outbound traffic for protocol TCP on port 443 and destination 0.0.0.0/0.
See https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_instances.html#container_instance_concepts