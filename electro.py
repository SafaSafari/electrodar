import uuid
import json
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


class Electro:
    def run(self):
        l = self.getList()
        for k, v in enumerate(l):
            print("{}. {}".format(k + 1, v["name"]))
        i = ss_input("Please select server", 1) - 1
        server = l[i]
        self.url = server["configLink"]
        self.api = server["apiLink"]
        name = str(uuid.uuid4())
        with open(name, "w") as f:
            f.write(self.genConfig(True))
        print("Conf file saved successfully: {}".format(name))

    def getList(self):
        return json.loads(
            requests.get(
                "https://elcdn.ir/app/servers.json", headers={"User-Agent": ""}
            )
            .content.replace(b"\n", b"")
            .replace(b",]", b"]")
        )

    def publicInfo(self):
        return json.loads(
            requests.get(self.url, headers={"User-Agent": ""}).content.replace(
                b"\n", b""
            )
        )

    def privateInfo(self):
        return json.loads(
            requests.get(self.api, headers={"User-Agent": ""}).content.replace(
                b"\n", b""
            )
        )

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
            public=public["publickey"],
            endpoint=public["endpoint"],
            dns=public["dns"],
            route="0.0.0.0/0" if route else public["routes"],
            psk=private["psk"],
            private=private["private_key"],
            address=private["ip"],
        )
        return base


if __name__ == "__main__":
    r = Electro()
    r.run()
