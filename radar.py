import requests


class Regions:
    Tehran = "tehran"
    Tabriz = "tabriz"
    Mashhad = "mashhad"
    Isfahan = "isfahan"
    Ahvaz = "ahvaz"

class Radar:
    def publicInfo(self, region: Regions = Regions.Tehran):
        return requests.get(
            "https://cdn.radar.game/app/vpn/{}wireguard.json".format(region), headers={"user-agent": ""}).json()

    def privateInfo(self, region: Regions = Regions.Tehran):
        return requests.get("https://{}wg.radar.game/getWGKey".format(region), headers={"user-agent": ""}).json()

    def genConfig(self, region: Regions = Regions.Tehran, route=False):
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
        public = self.publicInfo(region)
        private = self.privateInfo(region)
        base = base.format(public=public['publickey'], endpoint=public['endpoint'], dns=public['dns'], route="0.0.0.0/0" if route else public['routes'], psk=private['psk'], private=private['private_key'], address=private['ip'])
        return base

r = Radar()
for region in Regions.__dict__.values():
    if region[:2] == '__':
        continue
    print(region)
    print(r.genConfig(region))