import json
import httpx
from datetime import datetime


class backup:
    def __init__(self, token):
        self.token: str = token
        self.req: httpx.Client = httpx.Client()
        self.req.headers.update(self.create_headers())
        self.get_info()
        self.get_friends()
        self.get_guilds()
        print(" > Finished Backing up the account")

    def get_info(self):

        r = self.req.get(
            "https://discordapp.com/api/v9/users/@me", headers=self.headers)

        self.id = r.json()['id']
        date = datetime.now()
        remove = str(date).replace(
            str(date).split(".")[-1], "").replace(':', '.')
        self.filename = f"Backup {self.id} - {remove}txt"
        self.rawfilename = f"Backup RAW {self.id} - {remove}txt"

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"Info:\n")
            f.write(
                f"Username: {r.json()['username']}#{r.json()['discriminator']}\n")
            f.write(f"ID: {r.json()['id']}\n")
            f.write(f"Bio: {r.json()['bio']}\n")
            f.write(f"Email: {r.json()['email']}\n")
            f.write(f"Phone: {r.json()['phone']}\n\n")

        with open(self.rawfilename, "a", encoding="utf-8") as f:
            f.write("RAW Info:\n")
            f.write((json.dumps(r.json(), sort_keys=True, indent=4)) + "\n\n")

    def get_guilds(self):
        
        r = self.req.get(
            "https://discordapp.com/api/v9/users/@me/guilds", headers=self.headers)

        guildlist = []

        for guild in r.json():
            level = 32 - len(guild['name'])
            lvlstr = " "
            if len(guild['name']) < 32:
                for index in range(level):
                    lvlstr = lvlstr + " "
            guildlist.append(
                f"{guild['name']}{lvlstr}| {guild['id']} | Owner? {str(guild['owner'])}\n")

        guilds = ""
        guildlist.sort()

        for guild in guildlist:
            guilds = guilds + guild

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write("Guilds:\n")
            f.write(guilds + "\n\n")

        with open(self.rawfilename, "a", encoding="utf-8") as f:
            f.write("RAW Guilds:\n")
            f.write((json.dumps(r.json(), sort_keys=True, indent=4)) + "\n\n")

    def get_friends(self):
        
        r = self.req.get(
            "https://discordapp.com/api/v9/users/@me/relationships", headers=self.headers)

        friendslist = []
        blockedlist = []
        frnreqslist = []

        for user in r.json():
            if user['type'] == 1:
                friendslist.append(
                    f"{user['user']['username']}#{user['user']['discriminator']} | {user['id']}\n")

            elif user['type'] == 2:
                blockedlist.append(
                    f"{user['user']['username']}#{user['user']['discriminator']} | {user['id']}\n")

            else:
                frnreqslist.append(
                    f"{user['user']['username']}#{user['user']['discriminator']} | {user['id']}\n")

        friends = ""
        blocked = ""
        frnreqs = ""
        friendslist.sort()
        blockedlist.sort()
        frnreqslist.sort()

        for friend in friendslist:
            friends = friends + friend

        for block in blockedlist:
            blocked = blocked + block

        for frnreq in frnreqslist:
            frnreqs = frnreqs + frnreq

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write("Friends:\n")
            f.write(friends + "\n")
            f.write("Blocked people:\n")
            f.write(blocked + "\n")
            f.write("Friendrequests:\n")
            f.write(frnreqs + "\n\n")

        with open(self.rawfilename, "a", encoding="utf-8") as f:
            f.write("RAW Friendslist:\n")
            f.write((json.dumps(r.json(), sort_keys=True, indent=4)) + "\n\n")

    def create_headers(self):
        headers = {'accept': '*/*',
                   'authorization': self.token,
                   'content-type': 'application/json',
                   'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                   'sec-ch-ua-mobile': '?0',
                   'sec-ch-ua-platform': '"Windows"',
                   'sec-fetch-dest': 'empty',
                   'sec-fetch-mode': 'cors',
                   'sec-fetch-site': 'same-origin',
                   'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17'}
        return headers


backup(input(" > Please input the token of the account to backup\n > ").strip().replace('"', "").replace("'", ""))
