# Création de ressources Azure à partir de template ARM

## Installation des pré-requis

```python
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel
pip install .
```

## Configuration

```bash
cp .env.sample .env
vi .env
```

**Fichier d'environnement:**

```
AZURE_RESOURCE_GROUP="MYRG"
AZURE_SUBSCRIPTION_ID="00000000-0000-0000-00000000000000000"
AZURE_CLIENT_ID="00000000-0000-0000-00000000000000000"
AZURE_CLIENT_SECRET="XXX"
AZURE_TENANT_ID="00000000-0000-0000-00000000000000000"
```

## Exemple d'utilisation

**Création d'un storage Account:**

**Template utilisé:** [template](arm_py/templates/storage-account/template.json)

```python
import os
from pprint import pprint
from dotenv import load_dotenv   
from arm_py import get_client, get_template, validate_parameters, deployment

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
```