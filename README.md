# prompt-serve
**store and serve language model prompts**

## Overview 📖
`prompt-serve` helps you manage all of your large language model (LLM) prompts and associated settings/metadata in a straightforward, version controlled manner. 

This project provides a YAML schema for storing prompts in a structured manner and a small API server that handles interactions with a Git repository, so you can treat prompts more like re-usable code. 

* [Release blog post](https://deadbits.substack.com/p/the-prompt-serve-schema)

## Highlights ✨
* YAML schema for prompts and associated metadata
* Associate prompts to one another to represent chains
* Create "packs" of multiple prompts or chains to represent categories of tasks or workflows
* Store any kind of prompt text or template
* Store LLM provider, model, and settings
* Easily convert to [LangChain](https://github.com/hwcase17/langchain) [Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/)
* Command-line utility for creating prompt files
* Command-line utility for viewing prompt statistics
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
input_variables:
  - var1
  - var2
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
You can use the [validate.py](validate.py) utility to verify prompts meet the schema and have unique UUIDs. 

By specifying the `--create` argument, a new UUID will be provided if a given prompt doesn't have a unique ID for your scanned set.

```
usage: validate.py [-h] [-s SCHEMA] [-f FILE] [-d DIRECTORY] [-c] [-g]

Validate YAML files against the prompt-serve schema.

options:
  -h, --help            show this help message and exit
  -s SCHEMA, --schema SCHEMA
                        schema file to validate against
  -f FILE, --file FILE  single file to validate
  -d DIRECTORY, --directory DIRECTORY
                        directory to validate
  -c, --create          create new uuids if validation fails
  -g, --gen-stats       generate statistics from directory

```

You can also gather statistics on the types of prompts in your collection by passing `--gen-stats`. The screenshot below is an example of this output.
![Validation with stats](/assets/validate-with-stats.png)

## Statistics utility
The command line utility [stats.py](stats.py) will scan a directory of prompt-serve files and display statistics on the category, provider, and model fields in tables. 
Stats can also be optionally collected when running [validate.py](validate.py).

**Example output** 
![Stats](/assets/stats-cli.png)

## Use in LangChain
prompt-serve files can be easily converted to LangChain Prompt Templates.

```
import yaml
from langhain import PromptTemplate

def ps_to_langchain():
    with open('prompt-serve.yml', 'r') as file:
        try:
            data = yaml.safe_load(file)
            prompt = data.get('prompt')
            input_vars = data.get('input_variables)'
            langchain_template = PromptTemplate(template=prompt, input_variables=input_vars)
            return langchain_template
        except:
            pass
```

## Prompt creation helper
The command line utility [create.py](create.py) can be used to interactively create a prompt with the prompt-serve schema. 

🪲 This is just a proof of concept and has a few known bugs:
* multi-line input for "prompt" field not handled correctly
* no defaults are set for optional fields

```
$ python create.py -n summary.yml                   [20:27:04]
creating prompt file summary.yml ...
title (str): Summarize blog posts
description (str): Summarize a blog post with key takeaways
category (str): summarization
provider (str) : openai
model (str) : gpt-3.5-turbo
temperature (float) : 0.8
top_k (int) : 
top_p (float) : 0.9
max_tokens (int) : 512
stream (bool) : false
presence_penalty (float) : 
frequency_penalty (float) : 
prompt (str): Summarize the blog post provided below with 3-5 key takeaways as bullet points: {blog_content}
references (seq) : https://github.com/deadbits/prompt-serve
associations (seq) : 
packs (seq) : 
tags (seq) : 
 successfully wrote file summary.yml
```
