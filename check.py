from collections import defaultdict, namedtuple

def proccess_mappings(mappings):
    field_desc = defaultdict(lambda: defaultdict(set))
    for type_name, desc in mappings.items():
        proccess_fields(field_desc, type_name, desc['properties'], [])
    return field_desc

def proccess_fields(field_descs, type_name, fields, path=[]):
    for field_name, field_desc in fields.items():
        proccess_field(field_descs, type_name, field_name, field_desc, path)

def proccess_field(field_descs, type_name, field_name, field_desc, path=[]):
    path.append(field_name)
    full_name = tuple(path)
    desc = set()
    for k, v in field_desc.items():
        if k == 'fields':
            proccess_fields(field_descs, type_name, v, path)
        else:
            desc.add(Entry(k, proccess_value(v)))
    field_descs[full_name][frozenset(desc)].add(type_name)
    path.pop()

def proccess_value(v):
    t = type(v)
    if t is dict:
        g = (Entry(k, proccess_value(v_)) for k, v_ in v.items())
        return frozenset(g)
    if t is list:
        g = (proccess_value(v_) for v_ in v)
        return tuple(g)
    return v

Entry = namedtuple('Entry', ['key', 'value'])
