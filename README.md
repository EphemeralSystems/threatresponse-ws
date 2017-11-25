# ThreatResponse Examiner Workstation by Ephemeral Systems

The ThreatResponse workstation is a supported version of the tools provided
by github.com/threatresponse.  Everything is still under MIT license.

# Goals

* Make it simpler to deploy aws_ir tooling
* Pre install gnupg2 and trust margarita shotgun signing keys.
* Support SSM calls to drive threatresponse tools by enabling SSM agent.
* Users get new versions of aws_ir more raplidly.
* Image is reusable in other tool pipelines.

# Using the Image

Using the image is easy just use the provided cloudformation stack template.

## The following region/amis are provided and marked public:
```
us-east-1: "ami-831385f9"
us-west-1: "ami-c9556ea9"
us-west-2: "ami-dec51aa6"
eu-west-2: "ami-6c849b08"
ap-southeast-1: "ami-a4f9a8c7"
ap-northeast-1: "ami-d155f2bf"
```
# To Do

* Publish in the AWS Market
