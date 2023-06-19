# prompt-serve
**store and serve language model prompts**

## Overview 📖
`prompt-serve` is helps you manage all of your large language model (LLM) prompts and associated settings/metadata in a straightforward, version controlled manner. 

This project provides a YAML schema for prompt indexing purposes and a small API server that handles interactions with a Git repository.

## Highlights ✨
* YAML schema for prompts and associated metadata
* API server to upload or retrieve prompts
* Version controlled via Git
* Associate prompts to one another to represent chains
* Create "packs" of multiple prompts or chains to represent categories of tasks or workflows
* Store any kind of prompt text or template (LangChain, Guidance, etc.)
* Store LLM provider, model, and settings for evaluation purposes

## Schema 🗺️
Uploaded prompts are validated against [schema.yml](schema.yml). 

Check out the [examples](examples/) repository to see the schema in action. [examples](examples/) is a sub-repository created with `prompt-serve` and houses a collection of useful prompts.

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
