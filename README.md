## PARADIM Importer (proof of concept)

This is a proof of concept for a tool that can import data from the PARADIM resources into a Girder instance. The tool is written in Python and uses the Girder REST API.

### How to use?

1. Obtain a Girder API key from the Girder instance you want to import data into. (see [here](https://girder.readthedocs.io/en/stable/user-guide.html#api-keys)). It has to be an admin account.
2. Clone this repository.
3. Install the required packages by running `pip install -r requirements.txt`.
4. Run the importer by running `python importer.py <your-api-key> <girder-url> <target_root_folder>`. Note: the target root folder has to be under root folder of current Girder's assetstore as mounted in the Girder container and it has to be mounted the same way in the importer container/environment.
