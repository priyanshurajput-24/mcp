## Model Context Protocol (MCP)

* We have server that can run sparately and provide information to LLM.
* We have client that can interect with multiple server at the same time.
* Tools, Resources, Prompt are work as a middleware for providing context to LLM.



### Basic Demonstration of MCP.

* In this repo we can get basic idea how LLM's will go through for a basic math calcualtion and try to solve it, and at the same time if we provide some context and resources the how's the response is change drastically.
* You can see the difference in response in `response.md` file for both cases.
* So for using locally we need the `GROQ_API_KEY` for running this repo in a `.env` file.
* Here i'm unsing `uv` packages manager of `Python` for installing the dependencies and running the command, I'm providing the command for `Linux` and `Mac`.
* Create Virtual Environmental, If you have `uv` in your system run this command on your terminal.
    ```bash
    uv venv
    ```
* Then activate Virtual Environmental 
    ```bash
    sources .venv/bin/activate
    ```
* Install dependencies
    ```bash
    uv add -r requirements.txt
    ```
* First of all we have to start the a `http-server` for getting the weather data. for that run `weather.py`, So excute this command in your teminal.
    ```bash
    python weather.py
    ```
* Now we will see how's the response of Raw LLM's without any context. So open new terminal and activate virtual environment then Run the `client_raw_response.py`
    ```bash
    python client_raw_response.py
    ```
* Check out the response for the math expression, and raw weather API response. As it's very `lengthy` and too much `Token hungry`. If we pass directly raw questoin to the LLM's then this kind of case. Here i'm not passing API response to LLM.
* Now it's time to see see how the context aware LLM can do much better in this, so in new terminal run `client_context_aware_response.py` file, 
    ```bash
    python client_context_aware_response.py
    ```
* As it's given it can consise the response of a given math expression, and format the API response as mention in given instructions.  
* Here we do not need to run `mathserver.py` separately because there transport protocol is `stdio` but for `weather.py` it's `streamable-http`.


```text
So that's all it will provide a comprehensive overview of MCP and their functionally like server, host, client, tools.   
```
