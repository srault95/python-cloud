# Conversion de paramètres ARM en JSON Schema

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel
pip install .
```

## Exemple d'utilisation en mode commande

```bash
arm2schema -T templates/storage-account/template.json
# OR:
python -m arm2schema.core -T templates/storage-account/template.json
```

## Exemple d'utilisation par programmation

```python
import json
import os

from arm2schema.core import convert

with open("template.json") as fp:
    data = json.load(fp)
    result = convert(data["parameters"], data.get("title"), description=data.get("description"))
    print(result)
```

## Template ARM

```json
{
    "$schema": "http://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
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
    "variables": {
        "location": "[resourceGroup().location]",
        "apiVersion": "2019-06-01"
    },
    "resources": [
        {
            "name": "[parameters('storageAccountName')]",
            "type": "Microsoft.Storage/storageAccounts",
            "apiVersion": "[variables('apiVersion')]",
            "location": "[variables('location')]",
            "properties": {
                "accessTier": "[parameters('accessTier')]",
                "minimumTlsVersion": "[parameters('minimumTlsVersion')]",
                "supportsHttpsTrafficOnly": "[parameters('supportsHttpsTrafficOnly')]",
                "allowBlobPublicAccess": "[parameters('allowBlobPublicAccess')]",
                "networkAcls": {
                    "bypass": "[parameters('networkAclsBypass')]",
                    "defaultAction": "[parameters('networkAclsDefaultAction')]",
                    "ipRules": []
                }
            },
            "dependsOn": [],
            "sku": {
                "name": "[parameters('accountType')]"
            },
            "kind": "[parameters('kind')]",
            "tags": "[parameters('tags')]"
        }
    ],
    "outputs": {
        "storageAccountConnectionString": {
            "type": "string",
            "value": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageAccountName'), ';AccountKey=', listKeys(resourceId('Microsoft.Storage/storageAccounts', parameters('storageAccountName')), variables('apiVersion')).keys[0].value)]"
        }
    }
}
```

## Résultat

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "templates/storage-account/template.json",
    "description": "templates/storage-account/template.json",
    "required": [
        "storageAccountName"
    ],
    "properties": {
        "storageAccountName": {
            "type": "string"
        },
        "accountType": {
            "type": "string",
            "description": "Storage Account type",
            "default": "Standard_LRS",
            "enum": [
                "Standard_LRS",
                "Standard_GRS",
                "Standard_ZRS"
            ]
        },
        "kind": {
            "type": "string",
            "default": "StorageV2"
        },
        "accessTier": {
            "type": "string",
            "default": "Hot"
        },
        "minimumTlsVersion": {
            "type": "string",
            "default": "TLS1_2"
        },
        "supportsHttpsTrafficOnly": {
            "type": "boolean",
            "default": true
        },
        "allowBlobPublicAccess": {
            "type": "boolean",
            "default": true
        },
        "networkAclsBypass": {
            "type": "string",
            "default": "AzureServices"
        },
        "networkAclsDefaultAction": {
            "type": "string",
            "default": "Allow"
        },
        "tags": {
            "type": "object",
            "default": {}
        }
    },
    "type": "object"
}
```
