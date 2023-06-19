# prompt-serve
Store and serve language model prompts

## What is it
`prompt-serve` is designed to help you manage all of your large language model (LLM) prompts and associated settings/ metadata in a straightforward, version controlled manner. 

**YAML schema**
Uploaded prompts are validated against [schema.yml](schema.yml). Check out the [examples](examples/) folder to see the schema in action with different prompt template types and providers.

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

**Highlights:**
* Straightforward YAML schema for prompts and metadata
* API server to upload or retrieve prompts
* Easily retrieve prompts for use in your own code
  * Retrieve as prompt text only, YAML with full metadata, or LangChain prompt template  
* Associate prompts to one another to represent chains
* Create "packs" of multiple prompts or chains to represent categories of tasks or workflows
* Store any kind of prompt text or template (LangChain, Guidance, etc.)

### More
The schema supports LLM provider, model, and settings fields so you can save prompts and evaluations to re-run in specific environments.

Unlike some other prompt management applications, `prompt-serve` does not execute the LLM prompts for you. The idea here is to keep things simple: store your prompts here, retrieve them how you want, use them in your code how you want.



