#!/usr/bin/env python

import os
from os import path
import json
import elasticsearch
import email
import gzip
import io
import click


def unicodish(s):
    return s.decode('latin-1', errors='replace')


def test_gzip_read():
    with gzip.open('email/archived/db/2015-09/1511439457162298101.eml.gz', 'r') as fp:
        message = email.message_from_file(fp)
    print '%r' % (message.items(),)


def parse_and_store(es, account, email_path):
    gm_id = path.split(email_path)[-1]
    with gzip.open(email_path + '.eml.gz', 'r') as fp:
        message = email.message_from_file(fp)
    meta = {unicodish(k).lower(): unicodish(v) for k, v in message.items()}
    with open(email_path + '.meta', 'r') as fp:
        meta.update(json.load(fp))

    content = io.StringIO()
    if message.is_multipart():
        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                content.write(unicodish(part.get_payload()))
    else:
        content.write(unicodish(message.get_payload()))

    meta['account'] = account
    meta['path'] = email_path

    body = meta.copy()
    body['contents'] = content.getvalue()
    es.index(index='mail', doc_type='message', id=gm_id, body=body)


@click.command()
@click.argument('path-to-folder', default='email/archived')
@click.argument('account', default='root')
def index(path_to_folder, account):
    es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

    for base, subdirs, files in os.walk(path_to_folder):
        for name in files:
            if name.endswith('.meta'):
                parse_and_store(es=es, account=account, email_path=path.join(base, name.rsplit('.', 1)[0]))


if __name__ == '__main__':
    index()
