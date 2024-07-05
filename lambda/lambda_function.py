import json,boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    current_session = boto3.session.Session()
    current_region = current_session.region_name
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('AWS_INVENTORY')


    # To insert data to Dynamodb
    session = boto3.session.Session(profile_name='default')
    is_table_existing = table.table_status in ("ACTIVE")
    ec2 = boto3.client('ec2')


    ec2 = session.resource('ec2', current_region)

    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    InstanceName = terraform = Mssp = ''
    env = tenant = publicip = service = '-'
    service = '-'
    mssp = Name = terraform = stage = customer = namespace = emr = emr_instance_group = '-'
    my_data=[]
    for instance in instances:
        if instance.tags != None:
            for tag in instance.tags:

                    if tag['Key'] == 'Name':
                     InstanceName = tag['Value']

                    TenantId = '-'

                    if "-app" in InstanceName:
                        if "ha" in InstanceName:
                            split_value = InstanceName.split('-')
                            split_value.reverse()
                            TenantId = str(split_value[1])

                        else:
                            split_value = InstanceName.split('-')
                            split_value.reverse()
                            TenantId = str(split_value[0])

                    if "-rin" in InstanceName:
                        if "ha" in InstanceName:
                            split_value = InstanceName.split('-')
                            split_value.reverse()
                            TenantId = str(split_value[1])
                        else:
                            split_value = InstanceName.split('-')
                            split_value.reverse()
                            TenantId = str(split_value[0])

                    if tag['Key'] == 'Service':
                     service = tag['Value']

                    if tag['Key'] == 'Customer':
                     customer = tag['Value']

                    if tag['Key'] == 'Environment':
                     env = tag['Value']
                    if instance.public_ip_address:
                     publicip = instance.public_ip_address
                    if tag['Key'] == 'Mssp':
                        Mssp = tag['Value']
                    if tag['Key'] == 'Terraform':
                        terraform = tag['Value']
                    if tag['Key'] == 'Tenant':
                        tenant = tag['Value']
                    if tag['Key'] == 'Namespace':
                        namespace = tag['Value']
                    if tag['Key'] == 'Mssp':
                        mssp = tag['Value']
                    if tag['Key'] == 'Stage':
                        stage = tag['Value']
                    if tag['Key'] == 'Terraform':
                        terraform = tag['Value']
                    if tag['Key'] == 'aws:elasticmapreduce:job-flow-id':
                        emr = tag['Value']
                    if tag['Key'] == 'aws:elasticmapreduce:instance-group-role':
                        emr_instance_group = tag['Value']
                    if instance.public_ip_address:
                        # print('IP address is ', instance.public_ip_address)
                        publicip = instance.public_ip_address
                    else:
                     publicip = '-'

        else:
         print("No Data Avaliable")

        instance_tags = 'Environment: ' + env + ',   ' + 'Service: ' + service + ',   ' + 'Customer: ' + customer + ',   ' + 'Name: ' + Name + ',   ' + 'Namespace: ' + namespace + ',   ' + 'Mssp: ' + mssp + ',   ' + 'Stage: ' + stage + ',   ' + 'Terraform: ' + terraform + ',   ' + 'aws:elasticmapreduce:job-flow-id: ' + emr + ',   ' + 'aws:elasticmapreduce:instance-group-role: ' + emr_instance_group


        Item = {

                    'HostName': InstanceName,
                    'Name': InstanceName,
                    'Environment': env,
                    'TenantId': TenantId,
                    'Service': service,
                    'Customer': customer,
                    'Region': current_region,
                    'InstanceName': InstanceName,
                    'PrivateIP': instance.private_ip_address,
                    'PublicIP': publicip,
                    'DNSName': instance.private_dns_name,
                    'State': instance.state,
                    'ImageId': instance.image.id,
                    'InstanceType': instance.instance_type,
                    'instance_tags': instance_tags,
                    'AccountId': '853268358782'
                    # 'Tags': 'Name:'+ customer +'Service:'+Service +''
                }
        my_data.append(Item)
    # Removing data from dynamodb table
    scan = table.query(
        IndexName='Region-index',
    KeyConditionExpression=Key('Region').eq(current_region)
    )
    with table.batch_writer() as batch:
        for item in scan['Items']:
            # print("items data is---", item['Region'])
            batch.delete_item(Key={'DNSName':item['DNSName']})
    # Updating records to dynamodb table
    with table.batch_writer() as batch:
        for r in my_data:
            # print("R value is--",r)
            batch.put_item(Item=r)

