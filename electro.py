import uuid
import json
import requests


def ss_input(prompt, default='', t=int):
    result = input('{}{}: '.format(
        prompt, (" [" + str(default) + "] (Enter for default)") if str(default) != '' else ''))
    if result == '':
        return default
    else:
        return t(result)


class Radar:

    def run(self):
        l = self.getList()
        for k, v in enumerate(l):
            print("{}. {}".format(k + 1, v['name']))
        server = l[ss_input("Please select server", 1) - 1]
        self.url = server['configLink']
        self.api = server['apiLink']
        print(self.genConfig(True))

    def getList(self):
        return json.loads(requests.get("https://elcdn.ir/app/servers.json", headers={"User-Agent": ""}).content.replace(b'\n', b'').replace(b',]', b']'))

    def publicInfo(self):
        return json.loads(requests.get(self.url, headers={"User-Agent": ""}).content.replace(b'\n', b''))

    def privateInfo(self):
        return json.loads(requests.get(self.api, headers={"User-Agent": ""}).content.replace(b'\n', b''))

    def genConfig(self, route=False):
        base = """[Interface]
PrivateKey = {private}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {public}
PresharedKey = {psk}
Endpoint = {endpoint}
AllowedIPs = {route}
"""
        public = self.publicInfo()
        private = self.privateInfo()
        base = base.format(public=public['publickey'], endpoint=public['endpoint'], dns=public['dns'],
                           route="0.0.0.0/0" if route else public['routes'], psk=private['psk'], private=private['private_key'], address=private['ip'])
        with open(str(uuid.uuid4()) + ".conf", 'w') as f:
            f.write(base)
            return "Conf file saved successfully: {}".format(f.name)

if __name__ == '__main__':
    r = Radar()
    r.run()
