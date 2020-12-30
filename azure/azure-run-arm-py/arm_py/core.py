#!/usr/bin/env python

import uuid
import json
import os

from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode

__all__ = [
    'deployment',
    'get_client', 
    'get_template', 
    'get_json_schema', 
    'validate_parameters'
]

CURRENT = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.abspath(os.path.join(CURRENT, 'templates'))


def get_client(tenant_id: str, client_id: str, client_secret: str, subscription_id: str) -> ResourceManagementClient:

    # TODO: capture exception ?
    credentials = ClientSecretCredential(
        tenant_id,
        client_id,
        client_secret
    )
    return ResourceManagementClient(credentials, subscription_id)


def get_template(template_name) -> dict:
    template_path = os.path.join(TEMPLATES_DIR, template_name)

    with open(template_path, 'r') as fp:
        return json.load(fp)


def validate_parameters(template: str, parameters: dict):
    pass


def get_json_schema(template: dict) -> dict:
    parameters = template.get('parameters')
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

def deployment(
    client: ResourceManagementClient, 
    resource_group: str, 
    template: dict, 
    parameters: dict, 
    unid: str=None,                             # Deployment ID /subscriptions/00000000-0000-0000-00000000000000000/resourcegroups/MY_RG/providers/Microsoft.Resources/deployments/5fee26e1-0ec2-490a-816f-81e30490a359
    mode: str=DeploymentMode.incremental,       # complete (remove all in resource group) | incremental (add in resource group)
    timeout: int=None
    ) -> dict:

    parameters = {k: {'value': v} for k, v in parameters.items()}

    deployment_properties = { 
        "properties": {
            'mode': mode, 
            'template': template,
            'parameters': parameters
        }
    }

    if not unid:
        unid = str(uuid.uuid4())

    # operation is instance of azure.core.polling._poller.LROPoller
    operation = client.deployments.begin_create_or_update(
        resource_group,
        unid,
        deployment_properties
    )
    
    # TODO: capture exception ?
    operation.wait(timeout)

    return {
        "id": unid, 
        "status": operation.status(),        
        "result": operation.result().as_dict()
    }
    # operation.result is instance of azure.mgmt.resource.resources.v2020_06_01.models._models_py3.DeploymentExtended


def main():
    from pprint import pprint
    from dotenv import load_dotenv
    
    load_dotenv(verbose=False)

    tenant_id = os.environ['AZURE_TENANT_ID']
    client_id = os.environ['AZURE_CLIENT_ID']
    client_secret = os.environ['AZURE_CLIENT_SECRET']
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    resource_group = os.environ['AZURE_RESOURCE_GROUP']

    parameters = {
        "storageAccountName": "sraulttestarm",
    }

    client = get_client(tenant_id, client_id, client_secret, subscription_id)
    template = get_template('storage-account/template.json')
    validate_parameters(template, parameters)
    result = deployment(client, resource_group, template, parameters)
    
    pprint(result)


if __name__ == "__main__":
    main()