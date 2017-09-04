#!/usr/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------
#@version:    ??                               
#@author:   Dylan_wu                                                        
#@software:    PyCharm                  
#@file:    jstest.py
#@time:    2017/6/22 13:51
#----------------------------------------------
import json
import hashlib

m1 = hashlib.md5()
m1.update('123'.encode('utf-8'))
p1 = m1.hexdigest()
m2 = hashlib.md5()
m2.update('456'.encode('utf-8'))
p2 = m2.hexdigest()
print(p1,type(p1))
print(p2,type(p2))


dylan_dict = {'username':'dylan','password':p1,'home_dir':'dylan'}
elaine_dict = {'username':'elaine','password':p2,'home_dir':'elaine'}
json.dump(dylan_dict,open('dylan.json','w'))
json.dump(elaine_dict,open('elaine.json','w'))