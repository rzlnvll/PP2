import json
f = open('Practice4/sample-data.json',)
data = json.load(f)
print("Interface Status")
print("================================================================================")
print(f"{'DN':<55}{'Description':<20}{'Speed':<10}{'MTU':<5}")
print("-------------------------------------------------- --------------------    ------  ------")
for item in data["imdata"]:
    at = item["l1PhysIf"]["attributes"]
    dn = at["dn"]
    descr = at["descr"]      
    speed = at["speed"]  
    mtu = at["mtu"]         

    print(f"{dn:<55}{descr:<20}{speed:<10}{mtu:<5}")