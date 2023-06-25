# prompt-serve
**store and serve language model prompts**

## Overview 📖
`prompt-serve` helps you manage all of your large language model (LLM) prompts and associated settings/metadata in a straightforward, version controlled manner. 

This project provides a YAML schema for prompt indexing purposes and a small API server that handles interactions with a Git repository.

## Highlights ✨
* YAML schema for prompts and associated metadata

* Associate prompts to one another to represent chains
* Create "packs" of multiple prompts or chains to represent categories of tasks or workflows
* Store any kind of prompt text or template
* Store LLM provider, model, and settings
* API server to upload or retrieve prompts*
* Version controlled via Git*

`* = _coming soon_`

## Schema 🗺️
Prompts follow the schema provided in [schema.yml](schema.yml). 

Check out the [prompts](prompts/) repository to see it in action. 

```
title: prompt-title-or-name
uuid: prompt-uuid
description: prompt-description
category: prompt-category
provider: model-provider
model: model-name
model_settings:
  temperature: 0.8
  top_k: 40
  top_p: 0.9
prompt: prompt-text
references:
  - https://example.com
  - https://example.com
associations:
  - prompt_uuid
  - prompt_uuid
packs:
  - pack-uuid
  - pack-uuid
tags:
  - tag
  - tag
```

## Validation
You can use the [validate.py](validate.py) utility to verify prompts meet the schema and have unique UUIDs. By specifying the `--create` argument, a new UUID will be provided if a given prompt doesn't have a unique ID for your scanned set.

```
$ python validate.py --help                         [15:57:13]
usage: validate.py [-h] [-s SCHEMA] [-f FILE] [-d DIRECTORY] [-c]

Validate YAML files against the prompt-serve schema.

options:
  -h, --help            show this help message and exit
  -s SCHEMA, --schema SCHEMA
                        schema file to validate against
  -f FILE, --file FILE  single file to validate
  -d DIRECTORY, --directory DIRECTORY
                        directory to validate
  -c, --create          create new uuids if validation fails
```
