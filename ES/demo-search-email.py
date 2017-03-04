#!/usr/bin/env python

import json

import click
import elasticsearch


@click.command()
@click.argument('query', required=True)
@click.option('--raw-result/--no-raw-result', default=False)
def search(query, raw_result):
    es = elasticsearch.Elasticsearch()
    matches = es.search('mail', q=query)
    hits = matches['hits']['hits']
    if not hits:
        click.echo('No matches found')
    else:
        if raw_result:
            click.echo(json.dumps(matches, indent=4))
        else:
            for hit in hits:
                # This next line and the two after it are the only changes
                click.echo('To:{}\nFrom:{}\nSubject:{}\nPath: {}\n\n'.format(
                    hit['_source']['to'],
                    hit['_source']['from'],
                    hit['_source']['subject'],
                    hit['_source']['path']
                ))


if __name__ == '__main__':
    search()
