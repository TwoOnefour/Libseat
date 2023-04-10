import json
import os.path

import requests
import urllib3


class LibSeat:
    def __init__(self):
        self.session = requests.session()

    def get_token(self):
        self.session.cookies.update({
            "FROM_CODE": "WwsJA1o%3D",
            "Hm_lvt_7ecd21a13263a714793f376c18038a87": "1681037644,1681094879,1681106848,1681109448",
            # "wechatSESS_ID": "a2c10a4da82d08d65e0eceb2dc161f3cd94a884272d4f119"
            # "SERVERID": "b9fc7bd86d2eed91b23d7347e0ee995e|1681128202|1681128202",
        })
        if os.path.exists("./token.txt"):
            with open("./token.txt", "r") as f:
                self.session.cookies.set("Authorization", f.read().strip("\n"))
                result = self.session.get("https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat", verify=False)
            if "open" not in result.url:
                return
        # self.session.cookies.set("Authorization", "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjI1OTQ5ODQxLCJzY2hJZCI6OTYsImV4cGlyZUF0IjoxNjgxMTM1NDAyfQ.iioxrsi_a5nQPa1Rv6ouTzGf4d0_TJkhVTi7cK4OP-d03MEw5-9QjPF9Rc6xcYK2rQfYQgULsW62sGlQWHKNxqUZ_2kHofvyxXz0XiM39YI5Ws979ytbPVlmODcIB0zj31FSjd_o_hp5FhFPRHTeO-edqxiyUvMcjMi7W6ZlT75zkRYh-NkUTCnxM3cNlYG3WwEW8249-gh_dLK6BAaPw3BSj6MNXUv1Qzd-jXGm57gT62sv9rCrVBAQRttRJhDhKXdC96hL-Myrdep02odJ7JEVXRjYNByMCeSzodvryefmX8WDuK4v2N4-iJUETqWPMp7_nmdRrZPcgUt86AI0Nw")
        self.session.headers.update({"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.34(0x18002230) NetType/WIFI Language/en"})
        self.session.get("https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat", verify=False)
        self.save_token()
        # self.session.get("https://wechat.v2.traceint.com/index.php/urlNew/auth.html?r=https%3A%2F%2Fweb.traceint.com%2Fweb%2Findex.html%23%2Fpages%2Findex%2Findex%3Fr%3D{}%26n%3D6433fb0a19b71&code=061jm9000TtHLP1Cnj100yRbIE2jm90t&state=1".format(int(time.time())))

    def get_lib(self):
        data = {
	        "operationName": "list",
	        "query": "query list {\n userAuth {\n reserve {\n libs(libType: -1) {\n lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n lib_group_id\n lib_comment\n lib_rt {\n seats_total\n seats_used\n seats_booking\n seats_has\n reserve_ttl\n open_time\n open_time_str\n close_time\n close_time_str\n advance_booking\n }\n }\n libGroups {\n id\n group_name\n }\n reserve {\n isRecordUser\n }\n }\n record {\n libs {\n lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n lib_group_id\n lib_comment\n lib_color_name\n lib_rt {\n seats_total\n seats_used\n seats_booking\n seats_has\n reserve_ttl\n open_time\n open_time_str\n close_time\n close_time_str\n advance_booking\n }\n }\n }\n rule {\n signRule\n }\n }\n}"
        }
        self.lib = json.loads(self.session.get("https://wechat.v2.traceint.com/index.php/graphql/", json=data).text)["data"]["userAuth"]["reserve"]["libs"]

    def save_token(self):
        with open("./token.txt", "w") as f:
            f.write(self.session.cookies.get("Authorization"))

    def get_seat_status(self, libId):
        data = {"operationName":"libLayout","query":"query libLayout($libId: Int, $libType: Int) {\n userAuth {\n reserve {\n libs(libType: $libType, libId: $libId) {\n lib_id\n is_open\n lib_floor\n lib_name\n lib_type\n lib_layout {\n seats_total\n seats_booking\n seats_used\n max_x\n max_y\n seats {\n x\n y\n key\n type\n name\n seat_status\n status\n }\n }\n }\n }\n }\n}","variables":{"libId":libId}}
        return json.loads(self.session.get("https://wechat.v2.traceint.com/index.php/graphql/", json=data, verify=False).text)["data"]["userAuth"]["reserve"]["libs"]

    def get_seat(self, key, libId):
        data = {"operationName":"reserueSeat","query":"mutation reserueSeat($libId: Int!, $seatKey: String!, $captchaCode: String, $captcha: String!) {\n userAuth {\n reserve {\n reserueSeat(\n libId: $libId\n seatKey: $seatKey\n captchaCode: $captchaCode\n captcha: $captcha\n )\n }\n }\n}","variables":{"seatKey":key,"libId":libId,"captchaCode":"","captcha":""}}\
        self.session.get("https://wechat.v2.traceint.com/index.php/graphql/", json=data, verify=False)
        
    def run(self):
        urllib3.disable_warnings()
        self.get_token()
        self.get_lib()
        self.lib_id = [120425, 120446, 120467, 120488, 120509, 120530, 120551]  # 3,6 3,7 7,6 7,7
        self.myseat = [1,2,3,4]
        for i in self.lib_id:
            for j in self.get_seat_status(i)[0]["lib_layout"]["seats"]:
                if not j["name"] or j["name"] == "":
                    continue
                if int(j["name"]) - 1 <= 3 and j["seat_status"] != 1:
                    self.get_seat(j["key"], i)