# Microservices is a design pattern
# break a system into parts, each solving a specific problem
# each service can iteract with any other service
# we often think of microservices as Applicatin Program Interfaces (API)

import socket
import requests

options = ()

extra_info_dict = {
    'people': ['name', 'height', 'mass'],
    'planets': ['name', 'terrain', 'population'],
    'species': ['name', 'average_height', 'language']
}

def get_swapi_data(category, id, silent=True):
    
    url_template = 'https://swapi.dev/api/{category}/{id}'
    query_url = url_template.format(category=category, id=id)
    
    if not silent:
        print(f'Querying SWAPI: {query_url}')

    data = requests.get(query_url)
    return_code = data.status_code
    print(return_code)
    if return_code != 200:
        print(f'Query returned with error {return_code}')
        return f'Error {return_code}'
    else:    # rc 200
        
        response_dict = data.json()  # text? content? iter_lines? status_code?
        #print(type(data.json()))
        
        return_data = [ f'{data_key.ljust(16)}: {response_dict[data_key]}' for data_key in extra_info_dict[category] ]

        return '\n'.join(return_data)
    

def my_server(): # could be a class
    '''This simple server will respond to client requests
       Echo back the request as upper-case'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    setup_t = ('localhost', 9876) # IP and port (127.0.0.1)
    server.bind(setup_t) #tell the serveer which IP and port
    # we may choose to provide a 'backlog' integer
    # This allows multiple connections
    server.listen(4) # begin listening for requests
    print(f'Server is listening on {setup_t[0]} {setup_t[1]}')
    while True: # this is a run loop
        (client, addr) = server.accept()
        buf = client.recv(1024) # read the first 1024 bytes
        buf_str = buf.decode()
        #print(f'Server received {buf_str}')
        query_category = buf_str.split(', ')[0]
        query_id = buf_str.split(', ')[1]
        
        if query_category in ('people', 'planets', 'species'):
            response_str = get_swapi_data(category=query_category, id=query_id, silent=False)
            print(f'Proxy got reponse {response_str}')
            
            client.send(response_str.encode())


        elif buf == b'quit':
            client.send(b'You killed the server!!!')
            break 
        else:    
            client.send('Else'.encode())

if __name__ == '__main__':
    my_server()
