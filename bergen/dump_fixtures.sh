#!/usr/bin/env bash
python manage.py dumpdata --format=json transformers.transformer > fixtures/transformer.json
python manage.py dumpdata --format=json nodes.node > fixtures/node.json