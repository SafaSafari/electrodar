import requests

class Electro:
    def publicInfo(self):
        return requests.get(
            "https://elcdn.ir/app/vpn/t-wireguard.json", headers={"user-agent": ""}).json()

    def privateInfo(self):
        return requests.get("https://wg.elcdn.ir/getWGKey", headers={"user-agent": ""}).json()

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
        base = base.format(public=public['publickey'], endpoint=public['endpoint'], dns=public['dns'], route="0.0.0.0/0" if route else public['routes'], psk=private['psk'], private=private['private_key'], address=private['ip'])
        return base

r = Electro()
print(r.genConfig())