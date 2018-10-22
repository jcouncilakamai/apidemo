#!/usr/bin/python


from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

myaccount = "bamtechtesting"
accountkey = "H7IKbD0TclKCXMzBwM4Ta9ELdUHM/0KjQmNDAjwiTCwUPMCZzGPok/89jAmcQQKItQTVIbhaAYe1h/kQL5a6pw=="
table_service = TableService(account_name=myaccount, account_key=accountkey)



tasks = table_service.query_entities('bamtechtest444', filter="PartitionKey eq 'bamtechlogs'")
for task in tasks:
    print "Stream ID/URL: " + task.Stream_ID_URL
    print "Edge_Plays: " + task.Edge_Plays
exit(0)
