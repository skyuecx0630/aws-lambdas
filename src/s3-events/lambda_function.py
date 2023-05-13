import boto3
import urllib.parse
import os
import copy

# Initialise the Glue client using Boto 3
glue_client = boto3.client('glue')

def lambda_handler(event, context):

     for record in event['Records']:
        try:
            source_key = urllib.parse.unquote_plus(
                record['s3']['object']['key'], encoding='utf-8')

            # Extract the Glue Database and Table name from Environment Variables
            DATABASE_NAME = os.environ['GLUE_DATABASE_NAME']

            # Assuming object key is folder_name/YYYY/MM/DD/HH/sample.json
            table_name = source_key.split('/')[0]
            partitions_values = source_key.split('/')[1:-1] # Remove the folder name at front and filename at the end
            print(partitions_values) # Output: [‘YYYY’, ‘MM', ‘DD’, ‘HH']

            try:
                # Check if the partition already exists. If yes, skip adding it again
                get_partition_response = glue_client.get_partition(
                    DatabaseName=DATABASE_NAME,
                    TableName=table_name,
                    PartitionValues=partitions_values
                )
                print('Glue partition already exists.')

            except Exception as e:
                # Check if the exception is EntityNotFoundException. If yes, go ahead and create parition
                if type(e).__name__ == 'EntityNotFoundException':
                    print('Retrieve Table Details:')
                    get_table_response = glue_client.get_table(
                        DatabaseName=DATABASE_NAME,
                        Name=table_name
                    )

                    # Extract the existing storage descriptor and Create custom storage descriptor with new partition location
                    storage_descriptor = get_table_response['Table']['StorageDescriptor']
                    custom_storage_descriptor = copy.deepcopy(storage_descriptor)
                    custom_storage_descriptor['Location'] = storage_descriptor['Location'] + "/".join(partitions_values) + '/'

                    # Create new Glue partition in the Glue Data Catalog
                    create_partition_response = glue_client.create_partition(
                        DatabaseName=DATABASE_NAME,
                        TableName=table_name,
                        PartitionInput={
                            'Values': partitions_values,
                            'StorageDescriptor': custom_storage_descriptor
                        }
                    )
                    print('Glue partition created successfully.') 
                else:
                    # Handle exception as per your business requirements
                    print(e)   

        except Exception as e:
            # Handle exception as per your business requirements
            print(e)