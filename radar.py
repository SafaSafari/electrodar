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
            print("{}. {}".format(k + 1, v['loc']))
        server = l[ss_input("Please select server", 1) - 1]
        self.url = server['domain']
        self.dns = ','.join(server['dns'])
        print(self.genConfig(True))

    def getList(self):
        return requests.get("https://gw.radar.game/list", headers={"User-Agent": ""}).json()['result']

    def publicInfo(self):
        return requests.get(
            "https://gw.radar.game/getSettings", headers={"User-Agent": ""}).json()

    def privateInfo(self):
        return requests.get(self.url, headers={"User-Agent": ""}).json()

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
        base = base.format(public=private['result']['settings']['public_key'], endpoint=private['result']['settings']['endpoint'], dns=self.dns,
                           route="0.0.0.0/0" if route else public['result']['routes'], psk=private['result']['psk'], private=private['result']['private_key'], address=private['result']['ip'])
        with open(private['result']['uid'] + ".conf", 'w') as f:
            f.write(base)
            return "Conf file saved successfully: {}".format(f.name)

if __name__ == '__main__':
    r = Radar()
    r.run()
