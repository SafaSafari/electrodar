import uuid
import requests


def ss_input(prompt, default="", t=int):
    result = input(
        "{}{}: ".format(
            prompt,
            (" [" + str(default) + "] (Enter for default)")
            if str(default) != ""
            else "",
        )
    )
    if result == "":
        return default
    else:
        return t(result)


class Radar:
    def __init__(self, old=False) -> None:
        self.base = "https://gw.radar.game" if old else "https://prod.radar.game"
        self.session = requests.Session()

    def run(self):
        l = self.getList()
        for k, v in enumerate(l):
            print("{}. {}, ping: {}".format(k + 1, v["loc"], v["ping"]))
        i = ss_input("Please select server", 1) - 1
        server = l[i]
        self.url = server["domain"]
        self.dns = ",".join(server["dns"])
        name = str(uuid.uuid4())
        with open(name, "w") as f:
            f.write(self.genConfig(True))
        print("Conf file saved successfully: {}".format(name))

    def getList(self):
        return self.session.get(self.base + "/list", headers={"User-Agent": ""}).json()[
            "result"
        ]

    def publicInfo(self):
        return self.session.get(
            self.base + "/getSettings", headers={"User-Agent": ""}
        ).json()

    def privateInfo(self):
        return self.session.get(self.url, headers={"User-Agent": ""}).json()

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
        base = base.format(
            public=private["result"]["settings"]["public_key"],
            endpoint=private["result"]["settings"]["endpoint"],
            dns=self.dns,
            route="0.0.0.0/0" if route else public["result"]["routes"],
            psk=private["result"]["psk"],
            private=private["result"]["private_key"],
            address=private["result"]["ip"],
        )
        return base


if __name__ == "__main__":
    r = Radar()
    r.run()
