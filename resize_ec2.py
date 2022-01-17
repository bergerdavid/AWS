import time
import boto3


def resizeec2(ec2type):
    '''
    :param ec2type: small,medium, or large
    :return:
    '''
    if ec2type == 'small':
        size = 't3.large'
    elif ec2type == 'medium':
        size = 't3.2xlarge'
    elif ec2type == 'large':
        size = 'r5a.8xlarge'
    else:
        print(f'input not recognized , the options are:small, medium, large')

    client = boto3.client('ec2')

    # Insert your Instance ID here
    my_instance = 'i-0c0d7c502298a7f70'
    instances = client.describe_instance_status(InstanceIds=[my_instance])

    # Stop the instance
    print(f'stopping instance {my_instance}')
    client.stop_instances(InstanceIds=[my_instance])
    time.sleep(10)
    waiter = client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[my_instance])

    # show instance status
    for i in instances['InstanceStatuses']:
        instance_id = i['InstanceId']
        instance_state = i['InstanceState']
        instance_state_full = instance_state['Name']
        print(f'instance {instance_id} is {instance_state_full}')

    # Change the instance type
    print(f'resizing instance {my_instance}')
    client.modify_instance_attribute(InstanceId=my_instance, Attribute='instanceType', Value=size)

    # Start the instance
    print(f'starting instance{my_instance}')
    client.start_instances(InstanceIds=[my_instance])
    time.sleep(10)

    # show instance status
    for i in instances['InstanceStatuses']:
        instance_id = i['InstanceId']
        instance_state = i['InstanceState']
        instance_state_full = instance_state['Name']
        print(f'instance {instance_id} is {instance_state_full}')




