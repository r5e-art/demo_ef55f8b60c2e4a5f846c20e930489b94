terraform {

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 2.0.0"
    }
  }

  required_version = ">= 1.1.9"
}

locals {
  funky_name = "demo_ef55f8b60c2e4a5f846c20e930489b94"

  tags = {
    "Owner" : "Ilja Orlovs"
  }

  default_vpc_id = "vpc-04659f8a2fb482e66"
}



module "ecr" {
  source               = "cloudposse/ecr/aws"
  version              = "0.34.0"
  environment          = "dev"
  name                 = local.funky_name
  namespace            = "bi"
  image_tag_mutability = "MUTABLE"
}



module "ecs" {
  source = "terraform-aws-modules/ecs/aws"

  cluster_name = local.funky_name

  cluster_configuration = {
    execute_command_configuration = {
      logging = "OVERRIDE"
      log_configuration = {
        cloud_watch_log_group_name = "/aws/ecs/aws-ec2"
      }
    }
  }

  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
    FARGATE_SPOT = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
  }

  tags = {
    Environment = "Development"
    Project     = "EcsEc2"
  }
}



module "iam-role-ecs" {
  source  = "hendrixroa/iam-role-ecs/aws"
  version = "1.0.0"
}



resource "aws_lb_target_group" "www" {
  name_prefix = "www"
  target_type = "alb"
  port        = 80
  protocol    = "TCP"
  vpc_id      = local.default_vpc_id
}

resource "aws_security_group" "www" {
  name_prefix        = "www"
  description = "Allow TLS inbound traffic"
  vpc_id      = local.default_vpc_id

  ingress {
    description      = "TLS from VPC"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "TLS from VPC"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }


  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}

resource "aws_lb" "wwww" {
  name_prefix               = "www"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.www.id]
  subnets            = ["subnet-0daa678cce8f6198a", "subnet-0d19db1cbb53c4c22", "subnet-0d016f5be84b5267d"]

  enable_deletion_protection = false

  tags = {
    Environment = "production"
  }
}