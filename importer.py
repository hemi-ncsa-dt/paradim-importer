"""
A script to import PARADIM data folders into Girder by creating a collection and a folder for each data folder.
"""

import argparse
import os

import girder_client


def get_folders(path):
    """
    Get the list of folders in a directory.
    """
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]


def is_admin(gc):
    """
    Check if the user is an admin.
    """
    user = gc.get("/user/me")
    return user["admin"]


def createOrUpdateCollection(gc, name):
    """
    Create a collection with a given name if it does not exist.
    """
    collections = gc.listResource("collection", params={"text": name})
    for collection in collections:
        if collection["name"] == name:
            return collection
    else:
        return gc.createCollection(name)


def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(
        description="Import PARADIM data folders into Girder."
    )
    parser.add_argument("url", help="Girder URL")
    parser.add_argument("apikey", help="Girder API KEY")
    parser.add_argument("path", help="Path to the PARADIM data folders")
    args = parser.parse_args()

    gc = girder_client.GirderClient(apiUrl=args.url)
    gc.authenticate(apiKey=args.apikey)

    if not is_admin(gc):
        print("You must be an admin to run this script.")
        return

    default_assetstore = next((_ for _ in gc.get("/assetstore") if _["current"]), None)
    if default_assetstore is None:
        print("No default assetstore found.")
        return
    import_root = os.path.abspath(args.path)
    if not import_root.startswith(default_assetstore["root"]):
        print("The import path must be within the default assetstore root.")
        print("Default assetstore root: %s" % default_assetstore["root"])
        print("Import path: %s" % import_root)

    # Get the list of folders
    for folder_name in get_folders(import_root):
        # Create a collection for each data folder
        # TODO: CHANGE THE COLLECTION NAME PATTERN
        collection_name = folder_name.replace("_", "-").title()
        collection = createOrUpdateCollection(gc, collection_name)

        folder = gc.createFolder(
            collection["_id"], folder_name, parentType="collection", reuseExisting=True
        )
        folder_path = os.path.join(args.path, folder_name)

        gc.post(
            f"/assetstore/{default_assetstore['_id']}/import",
            {
                "importPath": folder_path,
                "destinationId": folder["_id"],
                "destinationType": "folder",
            },
        )


if __name__ == "__main__":
    main()
