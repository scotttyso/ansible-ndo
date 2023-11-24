#!/usr/bin/env python3
from dotmap import DotMap
import json
import re
jdata = DotMap(json.load(open('schema.json', 'r')))
schemas = DotMap()
print(json.dumps(jdata, indent=4))
for item in jdata.schemas:
    schemas[item.displayName].templates = DotMap()
    for i in item.templates:
        schemas[item.displayName].templates[i.name] = DotMap(bds=DotMap(), epgs = [])
        for e in i.bds:
            schema = re.search('schemas\/([a-z0-9]+)\/templates', e.vrfRef).group(1)
            vrf = re.search('vrfs\/([\\w\\-\\.]+)$', e.vrfRef).group(1)
            schemas[item.displayName].templates[i.name].bds[e.name] = DotMap(
                description = e.description, display_name = e.displayName, vrf = DotMap(name=vrf, schema=schema))
        for e in i.anps:
            for d in e.epgs:
                if ':' in d.displayName: description = d.displayName.split(':')[1]
                else: description = d.description
                print(d.bdRef)
                bd = re.search('bds\/([\\w\\-\\.]+)$', d.bdRef).group(1)
                schemas[item.displayName].templates[i.name].epgs.append(DotMap(
                    application_profile = e.name,
                    description = description,
                    name = d.name,
                    vrf = schemas[item.displayName].templates[i.name].bds[bd].vrf.name
                ))
print(f'{"=" * 91}\n  AAEP with EPG Mappings\n{"=" * 91}')
print(json.dumps(schemas, indent=4))
outfile = open('./schema_out.json', 'w')
outfile.write(json.dumps(schemas, indent=4))
outfile.close()
