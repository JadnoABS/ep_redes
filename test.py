from client import Client 

buffer = [{'value': "adipiscing elit, sed'", 'ack': 40},{'value': "adipiscing elit, sed'", 'ack': 60}, {'value': " do eiusmod tempor i'", 'ack': 80}, {'value': "ed felis eget velit '", 'ack': 160}, {'value': "t'", 'ack': 201}, {'value': "aliquet. Sagittis pu'", 'ack': 180}, {'value': "et dolore magna aliq'", 'ack': 120}, {'value': "ncididunt ut labore '", 'ack': 100}, {'value': "rus sit amet volutpa'", 'ack': 200}, {'value': "ua. Venenatis cras s'", 'ack': 140}]

client = Client()
client.buffer = buffer
client.check_if_concatenation_of_messages_are_possible(20, ("localhost", 10001))