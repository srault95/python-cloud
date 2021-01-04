import argparse
import json

from jsonschema import validate

"""
    "parameters": {
        "storageAccountName": {
            "type": "string"
        },
        "accountType": {
            "type": "string",
            "defaultValue": "Standard_LRS",
            "allowedValues": [
                "Standard_LRS",
                "Standard_GRS",
                "Standard_ZRS"
            ],
            "metadata": {
                "description": "Storage Account type"
            }
        },
        "kind": {
            "type": "string",
            "defaultValue": "StorageV2"
        },
        "accessTier": {
            "type": "string",
            "defaultValue": "Hot"
        },
        "minimumTlsVersion": {
            "type": "string",
            "defaultValue": "TLS1_2"
        },
        "supportsHttpsTrafficOnly": {
            "type": "bool",
            "defaultValue": true
        },
        "allowBlobPublicAccess": {
            "type": "bool",
            "defaultValue": true
        },
        "networkAclsBypass": {
            "type": "string",
            "defaultValue": "AzureServices"
        },
        "networkAclsDefaultAction": {
            "type": "string",
            "defaultValue": "Allow"
        },
        "tags": {
            "type": "object",
            "defaultValue": {}
        }
    },

"""
def replace_type(source):
    # TODO: json schema type: null, number
    source = source.lower()
    if source == "bool":
        return "boolean"
    elif source == "int":
        return "integer"
    elif source in ["string", "securestring"]:
        return "string"
    elif source in ["object", "secureobject"]:
        return "object"
    elif source == "array":
        return "array"
    else:
        raise AttributeError(f"unknow type : {source}")


def convert(parameters: dict, title: str, description: str = None) -> dict:
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": title,
        "description": description or title, 
        'required': [],
        'properties': {},
        'type': 'object'
    }
    
    for field_name, field in parameters.items():
        new_field = {
            "type": replace_type(field["type"])
        }
        # si type object avec définition ?
        """
            "defaultValue": "StorageV2"

        """
        if "metadata" in field and field["metadata"].get("description"):
            new_field["description"] = field["metadata"]["description"]

        if field.get("defaultValue") is None:
            schema["required"].append(field_name)
        else:
            new_field["default"] = field.get("defaultValue")

        if field.get("allowedValues"):
            new_field["enum"] = field.get("allowedValues")
        
        if field.get("type") in ["string", "securestring", "array"]:
            if field.get("minLength"):
                new_field["minLength"] = field.get("minLength")

            if field.get("maxLength"):
                new_field["maxLength"] = field.get("maxLength")

        if field.get("type") == "int":
            if field.get("minValue"):
                new_field["minValue"] = field.get("minValue")

            if field.get("maxValue"):
                new_field["maxValue"] = field.get("maxValue")

        schema['properties'][field_name] = new_field

    return schema

# TODO: ?
def validate_schema(schema: dict, sample: dict = {}):
    """
     v = jsonschema.Draft4Validator(schema)
    In [36]: errors = sorted(v.iter_errors(data), key=lambda e: e.path)
    for error in errors:
        for suberror in sorted(error.context, key=lambda e: e.schema_path):
            print(list(suberror.schema_path), suberror.message, sep=", ")


    """
    validate(sample, schema)

def options():
    
    parser = argparse.ArgumentParser(
        description="ARM Parameters to JSON Schema",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True,
    )

    parser.add_argument(
        "--arm-template",
        "-T",
        dest="arm_template",
        help="ARM Template Filepath.",
    )

    parser.add_argument("--debug", "-D", action="store_true")

    return parser.parse_args()

def main():

    args = options()

    with open(args.arm_template) as fp:
        data = json.load(fp)
    
    result = convert(data["parameters"], data.get("title", args.arm_template), data.get("description"))
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()