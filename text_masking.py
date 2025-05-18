def mask_entities_by_token(text, entities, entity_types_to_mask):
    tokens = text.split()
    token_positions = []
    current_pos = 0
    for token in tokens:
        start = text.find(token, current_pos)
        end = start + len(token)
        token_positions.append({'token': token, 'start': start, 'end': end})
        current_pos = end

    for entity in entities:
        if entity['entity_group'] in entity_types_to_mask:
            e_start, e_end = entity['start'], entity['end']
            for tp in token_positions:
                if not (tp['end'] <= e_start or tp['start'] >= e_end):
                    tp['token'] = '*' * len(tp['token'])

    return ' '.join(tp['token'] for tp in token_positions)
