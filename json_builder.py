import yaml

import os
import urllib
import json

def get_yaml(f):
  pointer = f.tell()
  if f.readline() != '---\n':
    f.seek(pointer)
    return ''
  readline = iter(f.readline, '')
  readline = iter(readline.next, '---\n')
  print ''.join(readline)
  return ''.join(readline)


users = {}
products = []
base = os.getcwd() + '/users'
for user in next(os.walk(base))[1]:
	if os.path.exists(base + os.sep + user +  "/info.txt"):
			with open(base + os.sep + user +  "/info.txt", 'r') as f:
				userInfo = yaml.load(f)
				users[user] = userInfo
				f.close();
			productsPath = base + os.sep + user + os.sep + "products"
			for product in next(os.walk(productsPath))[1]:
				with open(productsPath + os.sep + product + "/info.txt", 'r') as f:
					d = "".join(f.readlines()).split("---\n")
					productInfo = yaml.load(d[0])
					productInfo["caption"] = d[1]
					productInfo["author"] = user
					productInfo["images"] = []
					f.close()
				path = next(os.walk(productsPath + os.sep + product))[0].replace(os.getcwd(),'')
				for product in next(os.walk(productsPath + os.sep + product))[2]:
					if product.endswith(".jpg") or product.endswith('.png') or product.endswith('.gif'):
						productInfo["images"].append(path + product)
						# https://images.weserv.nl/?url=henriknygren.se/site/assets/files/2105/barberosgerby_bok_03.1696x0.jpg&w=800&il&q=90
				products.append(productInfo)
data =  json.dumps({"users" : users, "products" : products}, ensure_ascii=False).encode('utf8')

with open('data.json', 'w') as f:
	f.write(data)
	f.close()

# 	if os.path.isfile(obj):
# 		print obj