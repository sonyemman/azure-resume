import azure.functions as func
import logging
import os
from azure.cosmos import CosmosClient, exceptions, PartitionKey

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    cosmosdb_endpoint =  os.environ['STORAGE_CONNECTION_STRING']
    cosmosdb_key = os.environ['COSMOS_CONNECTION_KEY']
    cosmosdb_database = os.environ['cosmosdb_database_name']
    cosmosdb_container = os.environ['cosmosdb_container']
    cosmosdb_partition_key = os.environ['cosmosdb_partition_key']

    # Initialize Cosmos DB client
    client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)
    logging.info('Python HTTP trigger function processed a request.')

    #create a database
    try:
        database = client.get_database_client(cosmosdb_database)
    except exceptions.CosmosAccessConditionFailedError:
        database = client.create_database(cosmosdb_database)
        
    #create a container 
    try:
        container = database.get_container_client(cosmosdb_container)
    except exceptions.CosmosAccessConditionFailedError: 
        container = database.create_container(id=cosmosdb_container, partition_key=PartitionKey(path=cosmosdb_partition_key, kind='Hash'))
    except exceptions.CosmosHttpResponseError:
        raise
   
    query = f"SELECT * FROM c WHERE c.id = '{1}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    
    # Check if the record was found
        # Assuming there's only one result, retrieve the item
    item = items[0]

        # Update the count value
    item['count'] += 1

        # Upsert the updated record
    container.upsert_item(item)

        # Print the updated count value
    print(f"Updated count value: {item['count']}")
    return func.HttpResponse(f"This HTTP triggered function executed successfully. updated count: {item['count']}",status_code=200)
    