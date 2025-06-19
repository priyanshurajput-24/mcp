## Demonstration of `resources`, `prompt` in  Model-Contet-Protocol (MCP).

* This is continuation of my last update.
* In this demo we are going to see how we can use the `resources` and `prompt` static and dynamically.
* Getting specific response after providing the resources and how can we use re-use the `prompt` for over dynamic query generation.
* A example how a guided data `resources` for analysing a CSV can get much better overview of data.

## Process

* First of all we have to create and activate virtual environmental and install all requirements from `requirements.txt` file using:

    ```bash
    uv add -r requirements.txt
    ```
* Run `csv_processor` file from new terminal for getting the context for dynamic `CSV`:

    ```bash
    python csv_processor.py
    ```
* Then run `client_context_aware_response`: 

    ```bash
    python client_context_aware_response.py
    ```
* So we can see all guided response in the data using multiple resources and getting response form dynamic prompt. 
* We can re-use the same templete for a similar query.
* In file `mathserver`, we provide how one can delare a `resources` and `prompt`, and then use the same in `client_context_aware_response` file by calling them.

---

* One more update, in `Comparision.md` we provide the possible plus point of MCP. Check it out.
* So that all for this version, thanks for implementting. 👍👍👍👍👍

---
