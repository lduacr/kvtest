import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from logzero import logger
import traceback
import falcon
app = falcon.API()

class HelloWorld(object):
    '''Useful to check if the service is UP!.'''

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        hostname = socket.gethostname()
        resp.body = f'Hello World from k8s container on "{hostname}"!\n'

# class Status(object):
#     '''Useful to check if the service is UP!.'''

#     def on_get(self, req, resp, status):
#         resp.status = falcon.HTTP_200
#         resp.body = f'Input from URL: "{status}".\n'

class KeyVault(object):
    def on_get(self, req, resp, secret):
        resp.status = falcon.HTTP_200
        try:
            # vault_url = 'https://prod-wus2-dataops-kv.vault.azure.net'
            vault_url = 'https://contnr-dev15-kv.vault.azure.net'
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
            value = client.get_secret(secret).value
            resp.body = f'The secret "{secret}" with value "{value}".\n'
        except:
            resp.body = traceback.format_exc()
            resp.body = f"{resp.body}\n\nFaild to obtain key vault for secret '{secret}'!!!\n"

class KeyVaultSecret(object):
    def on_get(self, req, resp, kv, secret):
        resp.status = falcon.HTTP_200
        if kv == 'dev15':
            vault_url = 'https://contnr-dev15-kv.vault.azure.net'
        elif kv == 'produs':
            vault_url = 'https://prod-wus2-dataops-kv.vault.azure.net'
        else:
            vault_url = 'https://prod-neu-dataops-kv.vault.azure.net'
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
            value = client.get_secret(secret).value
            resp.body = f'The secret "{secret}" with value "{value}".\n'
        except:
            resp.body = traceback.format_exc()
            resp.body = f"{resp.body}\n\nFaild to obtain key vault for secret '{secret}'!!!\n"

app.add_route('/', HelloWorld())
# app.add_route('/{status}', Status())
app.add_route('/{secret}', KeyVault())
app.add_route('/{kv}/{secret}', KeyVaultSecret())

# if __name__ == '__main__':
#     from waitress import serve
#     serve(app, host='0.0.0.0', port=8090)

# import falcon
# app = falcon.App()
# import socket
# # print(socket.gethostname())
# class HelloWorld(object):
#     '''Useful to check if the service is UP!.'''

#     def on_get(self, req, resp):
#         resp.status = falcon.HTTP_200
#         hostname = socket.gethostname()
#         resp.body = f'Hello World from k8s container on "{hostname}"!\n'

# app.add_route('/', HelloWorld())

# Start the Falcon server
if __name__ == '__main__':
    from wsgiref import simple_server

    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()