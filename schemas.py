#!/usr/bin/env python3
from copy import deepcopy
from dotmap import DotMap
from operator import itemgetter
import json
import re
import sys
import yaml
jdata = DotMap(json.load(open(f'{sys.argv[1]}', 'r')))
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
                bd = re.search('bds\/([\\w\\-\\.]+)$', d.bdRef).group(1)
                schemas[item.displayName].templates[i.name].epgs.append(DotMap(
                    application_profile = e.name,
                    description         = d.displayName.replace(f'{d.name}-', ''),
                    name                = d.name,
                ))
schemas.pop('common')
check = deepcopy(schemas)
for key, value in check.items():
    for k, v in value.templates.items():
        if v.get('bds'): schemas[key].templates[k].pop('bds')
        schemas[k].templates[k].epgs = sorted(v.epgs, key=itemgetter('name'))
print(f'{"=" * 91}\n  Display Description Mappings\n{"=" * 91}')
schema_out = schemas.toDict()
#print(json.dumps(schemas, indent=4))
outfile = open('./schema_out.yaml', 'w')
outfile.write(yaml.dump(schema_out, indent=4))
outfile.close()
