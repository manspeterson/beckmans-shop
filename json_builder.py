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
			productsPath = base + os.sep + user + os.sep + "online_products"
			if os.path.exists(productsPath):
				for product in next(os.walk(productsPath))[2]:
					if product.endswith('.txt') and os.path.exists(productsPath + os.sep + product.replace('.txt','')):
						with open(productsPath + os.sep + product, 'r') as f:
							d = "".join(f.readlines()).split("---\n")
							productInfo = yaml.load(d[0])
							productInfo["beskrivning"] = d[1]
							productInfo["designer"] = userInfo["namn"]
							productInfo["designer-slug"] = user
							productInfo["titel-slug"] = product.replace('.txt', '')
							productInfo["bilder"] = []
							f.close()
						path = next(os.walk(productsPath + os.sep + product.replace('.txt', '')))[0].replace(os.getcwd(),'')
						for productImage in next(os.walk(productsPath + os.sep + product.replace('.txt', '')))[2]:
							if productImage.endswith(".jpg") or productImage.endswith('.png') or productImage.endswith('.gif'):

								productImageName = urllib.quote(productImage)
								# print product
								productInfo["bilder"].append(path[1:] + os.sep + productImageName)
								# https://images.weserv.nl/?url=henriknygren.se/site/assets/files/2105/barberosgerby_bok_03.1696x0.jpg&w=800&il&q=90
						if len(productInfo["bilder"]) != 0:
							products.append(productInfo)
tags = set()
for p in products:
	for t in p["taggar"].split(', '):
		tags.add(t.lower())
tags = list(tags)
tags.sort()

data =  json.dumps({"users" : users, "products" : products, "taggar" : tags},encoding='utf8', ensure_ascii=False).encode('utf8')

with open('js/data.js', 'w') as f:
	f.write("var data = " + data + ";")
	f.close()

# 	if os.path.isfile(obj):
# 		print obj