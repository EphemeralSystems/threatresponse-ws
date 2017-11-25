"""
MIT License

Copyright (c) 2016 ThreatResponse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# This script copies the AMI to other region and tag copied AMI 'DeleteOnCopy' with retention  days specified.
import boto3
from dateutil import parser
import datetime
import collections


# Specify the source region of AMI's created and the destination region to which AMI's to be copied
source_region = 'us-west-2'
source_image_resource = boto3.resource('ec2', source_region)

# AMI to be retained for the number of days in the destination region.
ami_retention = 15


def copy_latest_image(dest_region):
    images = source_image_resource.images.filter(Owners=["576309420438"])
    dest_image_client = boto3.client('ec2', dest_region)

    # Retention days in DR region, its for 15 days.
    retention_days = int(ami_retention)

    to_tag = collections.defaultdict(list)

    for image in images:
        image_date = parser.parse(image.creation_date)

        # Copy todays images
        if image_date.date() == (datetime.datetime.today()).date():
            if not dest_image_client.describe_images(
                Owners=['576309420438']
            )['Images']:
                print("Copying Image {name} - {id} to {region}".format(
                        name=image.name,
                        id=image.id,
                        region=dest_region
                    )
                )
                new_ami = dest_image_client.copy_image(
                    DryRun=False,
                    SourceRegion=source_region,
                    SourceImageId=image.id,
                    Name=image.name,
                    Description=""
                )

                to_tag[retention_days].append(new_ami['ImageId'])

                print("New Image Id {new_id} for {region} Image {name} - {id}".format(
                        new_id=new_ami,
                        name=image.name,
                        id=image.id,
                        region=dest_region
                    )
                )

                print("Retaining AMI {} for {} days".format(
                    new_ami['ImageId'],
                    retention_days)
                )

                for ami_retention_days in to_tag.keys():
                    delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
                    delete_fmt = delete_date.strftime('%d-%m-%Y')
                    print("Will delete {} AMIs on {}".format(
                            len(to_tag[retention_days]),
                            delete_fmt
                        )
                    )

                    # To create a tag to an AMI when it can be deleted after retention period expires
                    dest_image_client.create_tags(
                        Resources=to_tag[retention_days],
                        Tags=[
                            {'Key': 'DeleteOnCopy', 'Value': delete_fmt},
                            ]
                        )
            else:
                print("Image {name} - {id} already present in {region} Region".format(
                        name=image.name,
                        id=image.id,
                        region=dest_region
                    )
                )


def lambda_handler(event, context):
    regions = boto3.client('ec2').describe_regions()
    for region in regions.get('Regions'):
        copy_latest_image(region['RegionName'])


if __name__ == '__main__':
    lambda_handler(None, None)
