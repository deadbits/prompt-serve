# prompt-serve
**store and serve language model prompts**

## Overview 📖
`prompt-serve` helps you manage all of your large language model (LLM) prompts and associated settings/metadata in a straightforward, version controlled manner. 

This project provides a YAML schema for prompt indexing purposes and a small API server that handles interactions with a Git repository.

* [Release blog post](https://deadbits.substack.com/p/the-prompt-serve-schema)

## Highlights ✨
* YAML schema for prompts and associated metadata
* Associate prompts to one another to represent chains
* Create "packs" of multiple prompts or chains to represent categories of tasks or workflows
* Store any kind of prompt text or template
* Store LLM provider, model, and settings
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

## Statistics utility
The command line utility [stats.py](stats.py) will scan a directory of prompt-serve files and display statistics on the category, provider, and model fields in tables. 


**Example output** 
```
[ category ]
      category  Count
      instruct      6
          base      3
conversational      2
       injects      2
            qa      2
      guidance      1
         react      1
           cot      1
      security      1


[ provider ]
provider  Count
  openai     15
   local      4


[ model ]
        model  Count
gpt-3.5-turbo     14
       openai      1
openassistant      1
 WizardVicuna      1
       alpaca      1


[ tags ]
(top 5)
              tags  Count
            openai     14
         local-llm      4
              base      3
          instruct      3
question-answering      3

```

## Prompt creation helper
The command line utility [create.py](create.py) can be used to interactively create a prompt with the prompt-serve schema. 

🪲 This is just a proof of concept and has a few known bugs:
* multi-line input for "prompt" field not handled correctly
* no defaults are set for optional fields
   * we should not include the optional field if there's no input instead 

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
