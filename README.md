# 🛠️ DevOps Learning Path

Welcome to the **DevOps Learning Repository** — your hands-on, structured guide to becoming proficient in DevOps concepts, tools, and practices. This roadmap is designed for beginners to intermediate learners aiming to build real-world skills by learning and doing.

## 📄 Important Docs & Resources

These documents contain key reference material and project knowledge:

- [📄 DevOps Notes - Doc 1 (One word topics)](https://docs.google.com/document/d/1YoE2P6Pr2gC_1nIFG-K7b4LkZGlphOIo269mi1mYDUw/edit?tab=t.0)
- [📄 DevOps Notes - Doc 2](https://docs.google.com/document/d/1s-m5WrqJxHS18snbBWMaORHczbpI4b-Pcvt-DpIjLRQ/edit?tab=t.0)

---

## 📚 Overview

This repository contains structured knowledge, resources, and exercises to help you build a solid DevOps foundation. It is divided into several key modules:

1. [Basics](#1-basics)
2. [Git Version Control](#2-git-version-control)
3. [Linux & Terminal](#3-linux--terminal)
4. [Networking Fundamentals](#4-networking-fundamentals)
5. [Containerization with Docker](#5-containerization-with-docker)
6. [Orchestration with Kubernetes](#6-orchestration-with-kubernetes)
7. [IAC with Terraform](#7-terraform)
8. [IAC with pulumi](#8-Pulumi)
9. [Monitoring](#9-monitoring)
10. [Gitlab](#10-gitlab)
11. [Alloy Agent](#11-Alloyagent)

---

## 1. Basics

Start with understanding the high-level picture of DevOps — its culture, tools, and workflows. Learn the importance of automation, CI/CD pipelines, containerization, and monitoring.

---

## 2. Git Version Control

Understand and **practice the following Git and GitHub concepts**:

- ✅ Cloning, branching, committing, pushing, pulling
- ✅ Creating & reviewing MRs/PRs
- ✅ Rebasing vs Merging
- ✅ Resolving merge conflicts
- ✅ Git Conventional Commits (e.g., `feat: add login`, `fix: crash on submit`)
- ✅ Git logs, diffs (`git log`, `git diff`)
- ✅ `.gitignore` best practices
- ✅ GitHub Features: Issues, Projects, Discussions, Actions

---

## 3. Linux & Terminal

Get hands-on with terminal-based Linux environments. Key areas:

### 🐧 Linux Exercises

- Parse HTTP logs using a bash script (filter `GET` requests).
- Set and persist environment variables via `.bashrc` or `.zshrc`.
- Use `df`, `top`, and `free` to monitor system performance.

### 🖥️ Terminal Knowledge

- **Essential Commands**: `ls`, `cd`, `mv`, `cp`, `rm`, `grep`, `find`, `chmod`, `chown`, `top`, `ps`, `df`, `du`
- **Navigation & Permissions**
- **Text Editors**: `vim`, `nano`
- **Services**: `systemctl` (`start`, `stop`, `enable`, `status`)
- **Logs**: `journalctl`
- **Command Techniques**: `|`, `>`, `>>`, `&&`, `||`
- **Environment Variables**: `export`, `.bashrc`
- **SSH & File Transfers**: `ssh`, `scp`, `rsync`
- **Networking**: `ip`, `ping`, `curl`, `wget`
- **Package Managers**: `apt`, `yum`, `dnf`

---

## 4. Networking Fundamentals

- ✅ IPs, Subnets, CIDRs
- ✅ VPCs, Routing, and NAT
- ✅ Public vs Private Subnets
- ✅ Security Groups, NACLs

---

## 5. Containerization with Docker

### 📘 Resources

- [Docker Documentation](https://docs.docker.com/guides/get-started/)

### Projects

- Containerization of simple vite react app
- Containerization of simple web dev project called currency-converter [Used multi-stage deploy]
- Containerization of notes-app created in django and used nginx reverse proxy in it.
- Containerization of startup vite project with docker compose.
- Containerization of nginx reverse proxy setup for 3 different routings.
- Containerization of Web app Expense Calculator with Java

### 🧪 Exercises

- Run a PostgreSQL DB inside a Docker container.
- Create a **multi-stage Dockerfile**.
- Package a Node.js or React app using Docker.
- Understand build context and image layers.
- Completed this 
---
## 6. Orchestration with Kubernetes

### 📘 Resources

- [Kubernetes Docs](https://kubernetes.io/docs/home/)
- [Kind Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/)

### 🧪 Concepts

- Pods
- Namespace
- Deployment
- Services
- jobs
- cronjons
- daemonsets
- replicasets
- pv
- pvc
- ingress
- configmap
- resources
- secrets
- statefulSets
- Node affinity Statefulness
- DaemonSets
- Replicasets
- probes-> ready,live,startup
- taint and tolerance
- Roles
- Serivce Account 
- Role binding
- Cluster Role
- taint and tolerance 
- hpa
- vpa
- sidecar container
- Node Affinity
- Node Selector
- Init Container
- Istio Mesh
- Helm Package Manager
- Custom Resource Definitions
- Port Forwarding
- Minikube Addons (Metrics, Dashboard, Ingress)
- Pod Affinity 
- Monitoring 
- logging and debugging 
- Kubectl describe, logs, events etc..
- Topics.txt (Contains All the topics I studied)



### Projects

- Small Notes app project with its own readme for full execution.
- Project with 3-tier ChatApp With ingress port forwarding
- Hands on project given in Document For learning of k8s

---


## 7. Terraform (IaC)

### 📘 Topics

- What is Terraform
- Why use Terraform
- How Terraform works
- Terraform vs Ansible
- Terraform vs CloudFormation
- Cloud-specific IaC tools
- Install Terraform via Chocolatey
- .tf files
- Block structure in Terraform
- Parameters vs Arguments
- Block types: variable, resource, output
- Syntax: <block> <label> <block> { arguments }
- terraform init
- terraform validate
- terraform apply -auto-approve
- terraform destroy
- terraform --target usage
- Terraform providers
- Provider configuration
- AWS provider setup
- AWS key pair
- EC2 instance resource
- Interpolation syntax
- Key pair (key name, public, private)
- Security group basics
- Ingress and Egress rules
- Security group tags
- Variables block
- Locals block
- Validation block
- Combine variable + locals + validation
- object() type usage
- .tfvars file
- -var command line usage
- outputs
- count, for_each, depends_on
- conditional expressions
- list, map, object, loop
- built-in functions
- .tfstate has the state of your infrastructure → terraform refresh
- terraform state list
- terraform state mv <source> <destination>
- terraform state show <name>
- terraform state rm <name>
- terraform import <resource> <id>
- .tfstate file conflict: don't push to GitHub
- Use S3 backend for safe tfstate storage
- Use DynamoDB for state lock ID (state locking)
- S3 → backend storage
- DynamoDB → lock management
- terraform workspace list
- terraform workspace new <name>
- Point GitHub to same workspace as local
- terraform modules need source (local or remote)
- Modules can be downloaded from Terraform Registry
- You can create your own modules
- Custom module structure:
  - Main folder: main.tf, provider.tf, variables.tf, output.tf
  - Sub folder (module): main.tf, variables.tf, output.tf
  - Use `source = "./module-folder"` when calling a module


### Projects

- Small Notes app project with its own readme for full Infrastruture code.
- Project with 3-tier ChatApp With ingress port forwarding with Terraform infra Management.


---

## 8. Pulumi (IaC)

### 📘 Topics

- pulumi why
- pulumi main.py
- pulumi new \<What you want>
- python -m venv venv
- ./venv/scripts/activate- 
- pulumi up --yes
- pulumi destroy --yes
- pulumi up --skip-preview- 
- pulumi login 
- pulumi logout- 
- pulumi preview- 
- pulumi stack ls
- pulumi stack init 
- pulumi stack select
- pulumi stack rm

- pulumi config set  \<key> \<value>
- pulumi config get  \<key>
- pulumi config rm \<key>
- pulumi preview --diff
- pulumi destroy --target
- pulumi state ls
- pulumi state 
- Pulumi yaml 
- stacks 
- Configs
- Secrets
- Local vs cloud backend
- Inputs ad  outputs
- Error handling and debugging
- pulumi import 
- pulumi refresh 
- pulumi state delete 
- pulumi watch 
- pulumi cancel
- pulumi plugin


### Hands on 

- Hands on atsks from the Document of learning.


---

## 9. Monitoring (Prometheus, Loki, Grafana, Promtail, Alloy agent)

### 📘 Topics

- start monitoring 
- learn about Grafana 
- know observability 
- promehteus and its node exporter
- Prometheus connection
- Prometheus visualization in garfan 
- grafan marks and exploe the web page 
- dashboard 
- dashboard import and export
- queries
- Prometheus query page on 9090
- Prometheus config files
- loki setup 
- promtail for loki
- loki logs collection and config
- loki ready api
- loki metrics
- loki connection as data source
- loki logs view as table

### Hands on 

- Hands on atsks from the Document of learning.

---

## 10. Gitlab 

### 📘 Topics

- GitLab Understanding
- Pipelines
- Runner
- Visualization 
- Variables Usage  
- Artifacts Handling  
- Pipeline Triggers  
- Environments & Deployments  
- Manual Jobs & Auto Approvals  
- Includes & Templates  
- Runner Tags   
- Complex job relations between differnt jobs 


### Project

- Chat-App Pulumi pipeline on My own machine as the runner.

---
## 10. Alloy Agent 

### 📘 Topics

- Alloy Agent:  
- Alloy Agent Installation  
- Grafana Connection  
- Alloy Dashboards  
- Resource Limits 


---

## Basic Devops Traininng Completed [08/07/2025]

---


## ✅ Final Verdict :

This is a **Final  document** of all the topics I Completed during the training Time period. 
