__version__ = "0.0.0"

from . import pyrackndr

CONSTANTS = {
  'params':
  {
    "Available": True,
    "Bundle": "",
    "Description": None,
    "Documentation": None,
    "Endpoint": "",
    "Errors": [],
    "Name": None,
    "ReadOnly": True,
    "Meta": None,
    "Schema": {},
    "Secure": None,
    "Validated": True
  },
  'subnets':
  {
    "ActiveEnd": None,
    "ActiveLeaseTime": None,
    "ActiveStart": None,
    "Available": True,
    "Bundle": "",
    "Description": None,
    "Documentation": "",
    "Enabled": True,
    "Endpoint": "",
    "Errors": [],
    "Meta": {
      "color": "black",
      "icon": "cloud",
      "title": "User added"
    },
    "Name": None,
    "NextServer": "",
    "OnlyReservations": False,
    "Options": [
      {
        "Code": 3,
        "Value": None
      },
      {
        "Code": 6,
        "Value": None
      },
      {
        "Code": 15,
        "Value": None
      },
      {
        "Code": 1,
        "Value": None,
      },
      {
        "Code": 28,
        "Value": None
      }
    ],
    "Pickers": [
      "hint",
      "nextFree",
      "mostExpired"
    ],
    "Proxy": False,
    "ReadOnly": False,
    "ReservedLeaseTime": 21600,
    "Strategy": "MAC",
    "Subnet": None,
    "Unmanaged": False,
    "Validated": True
  },
  'templates':
  {
    "Available": True,
    "Bundle": "",
    "Contents": None,
    "Description": None,
    "Endpoint": "",
    "Errors": [],
    "ID": None,
    "Meta": {
      "color": "black",
      "icon": "file code outline",
      "title": "User added"
    },
    "ReadOnly": True,
    "Validated": True
  },
  'tasks':
  {
    "Available": True,
    "Bundle": "",
    "Description": None,
    "Documentation": None,
    "Endpoint": "",
    "Errors": [],
    "ExtraClaims": [],
    "ExtraRoles": [],
    "Name": None,
    "Meta": {},
    "OptionalParams": [],
    "OutputParams": [],
    "Prerequisites": [],
    "ReadOnly": True,
    "RequiredParams": [],
    "Templates": [
      {
        "Contents": None,
        "EndDelimiter": None,
        "ID": None,
        "Link": None,
        "Meta": {},
        "Name": None,
        "Path": None,
        "StartDelimiter": None
      }
    ],
    "Validated": True
  }
}
