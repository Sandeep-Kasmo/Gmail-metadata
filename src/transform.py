def parse_name_email(v):
    if not v:
        return None, None
    if '<' in v and '>' in v:
        name = v.split('<')[0].strip().strip('"')
        email = v.split('<')[1].replace('>', '').strip()
        return name, email
    return v, v

def transform(emails):
    out = []
    for e in emails:
        name, email = parse_name_email(e.get('from'))
        out.append({
            'message_id': e.get('message_id'),
            'thread_id': e.get('thread_id'),
            'date_received': e.get('date'),
            'sender_name': name,
            'sender_email': email,
            'receiver_emails': e.get('to'),
            'cc': e.get('cc'),
            'subject': e.get('subject'),
            'body_text': e.get('body_text'),
            'attachments': e.get('attachments', [])
        })
    return out
