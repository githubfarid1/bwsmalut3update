
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql+pymysql://root:1234@localhost:33061/db1', echo=False)

# Opening JSON file
f = open('data.json')

# returns JSON object as
# a dictionary
data = json.load(f)
# Iterating through the json
# list
for boxes in data:
	box_number = boxes['box']
	for bundles in boxes['data']:
		# save to bundles
		bundle_number = bundles['berkas']
		for docs in bundles['data']:
			pass
            # save to docs
            
            
		
# Closing file
f.close()
