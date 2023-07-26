## API server
Small API server that handles adding new prompts and retrieving stored prompts. 

This is meant to be used alongside a Git repository of prompts and the [ps.conf](../ps.conf) configuration file.
Update the `repo_path` variable to point to the parent directory of your repository.

### running
The API server assumes you have a configuration file named `ps.conf` in the main prompt-serve directory.

```
git clone https://github.com/deadbits/prompt-serve
cd prompt-serve/server
uvicorn api:app --reload
```

The API server will start on `http://localhost:8000`. 
You can access the Swagger documentation via `http://localhost:8000/docs`.

