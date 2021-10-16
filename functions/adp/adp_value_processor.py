import json

adp_config = open('adp_config.json', 'r').read()
adp_config = json.loads(adp_config)

field_name_processor = {
    field: {
        'key': adp_config['field_map'][field]['key'],
        'val': lambda val: val
    }
    for field in adp_config['field_map']
}


def _simple_adp_response_fetcher(value, object_key):
    return value[0][object_key]


action_response_processor = {
    action: lambda val: _simple_adp_response_fetcher(val, adp_config['action_response_map'][action]['key'])
    for action in adp_config['action_response_map']
}
