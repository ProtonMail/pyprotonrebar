"""
Interact with the RackN Digital Rebar API.
"""

import json
from typing import ClassVar

import jsonpatch
import requests


def generate_resource_diff(rdoc, ldoc):
    """Takes two Python dicts and returns a JSON RFC patch object."""
    return jsonpatch.make_patch(rdoc, ldoc)


def fetch_token_requests(role, userpass, endpoint, ttl=300, ssl=True):
    """Fetch a short-lived token for interacting with the Rebar API."""
    user = userpass.split(':')[0]
    passwd = userpass.split(':')[1]
    api = f'{endpoint}/api/v3/users/{user}/token'

    payload = {
        'ttl': ttl,
        'roles': role,
    }

    r = requests.get(api, auth=(user, passwd), params=payload, verify=ssl, timeout=10)

    try:
        req = json.loads(r.text)
        req['header'] = {'Authorization': f"Bearer {req['Token']}"}
        req['token'] = req['Token']
    except KeyError:
        req = None

    return req


DRYRUN = {'http_code': 200, 'message': 'DRYRUN'}


class RackNDr:
    """Interact with RackN Digital Rebar objects."""

    headers: ClassVar[dict] = {
        'Content-Type': 'application/json',
    }

    def __init__(self, endpoint, auth, resource):
        self.api = f'{endpoint}/api/v3'
        self.headers.update(auth)
        self.resource = resource
        self.timeout = 10
        self.dryrun = False
        self.tls_verify = True
        self.ignore_keys = {'local': [], 'remote': []}

    def exists(self, rname):
        """
        Checks for the existence of a DigitalRebar resource.

            Parameters:
                rname (str): A DigitalRebar resource name of type self.resource

            Returns:
                resource (bool): True when rname exists and false otherwise
        """
        api = f'{self.api}/{self.resource}/{rname}'

        # HEAD is enough for newer API versions
        r = requests.get(api, headers=self.headers, verify=self.tls_verify, timeout=self.timeout)
        resource = r.status_code == 200

        return resource

    def create_resource(self, rdata):
        """Takes python dict data payload and returns requests POST object."""
        api = f'{self.api}/{self.resource}'

        req = requests.post(api, headers=self.headers, data=json.dumps(rdata), verify=self.tls_verify, timeout=self.timeout)

        return req

    def get_resource(self, rname):
        """Takes resource name and returns requests GET object."""
        api = f'{self.api}/{self.resource}/{rname}'

        r = requests.get(api, headers=self.headers, verify=self.tls_verify, timeout=10)

        return r

    def update_resource(self, rname, rdata):
        """Takes resource name and python dict data payload and returns
        requests PUT object.
        """
        api = f'{self.api}/{self.resource}/{rname}'

        r = requests.put(api, headers=self.headers, data=json.dumps(rdata), verify=self.tls_verify, timeout=self.timeout)

        return r

    def delete_resource(self, rname):
        """Takes resource name and returns requests DELETE object."""
        api = f'{self.api}/{self.resource}/{rname}'

        r = requests.delete(api, headers=self.headers, verify=self.tls_verify, timeout=self.timeout)

        return r

    def delete(self, rname):
        """Takes resource name and returns dict containing resource deletion
        status.
        """
        results = {}
        robject = self.get_resource(rname)

        if robject.status_code == 200:
            results = {**results, **DRYRUN}
            if not self.dryrun:
                delete_object = self.delete_resource(rname)
                results['http_code'] = delete_object.status_code
                results['message'] = json.loads(delete_object.text).get('Messages')
            results['changed'] = True
            results['diff'] = {'before': json.loads(robject.text), 'after': None}
        else:
            results['http_code'] = 200
            results['message'] = f'{self.resource} object does not exist'
            results['changed'] = False

        return results

    def pop_keys(self, obj, list_of_items_to_pop=None):
        """Takes dict object and list of items to pop and pops items if they
        exist in dict.
        """
        if list_of_items_to_pop is None:
            list_of_items_to_pop = []

        for i in list_of_items_to_pop:
            obj.pop(i, None)

    def update(self, rname, lobject):
        """Takes resource name and local object and returns dict containing
        http_code, changed, message.
        """
        results = {}
        remote_object = json.loads(self.get_resource(rname).text)

        self.pop_keys(lobject, self.ignore_keys['local'])
        self.pop_keys(remote_object, self.ignore_keys['remote'])

        diff = generate_resource_diff(remote_object, lobject)

        if diff:
            if self.dryrun:
                results = {**results, **DRYRUN}
            else:
                update_remote_object = self.update_resource(rname, rdata=lobject)
                results['http_code'] = update_remote_object.status_code
                results['message'] = json.loads(update_remote_object.text).get('Messages')

            results['changed'] = True
            results['diff'] = {'before': remote_object, 'after': lobject}
        else:
            results['http_code'] = 200
            results['changed'] = False
            results['message'] = f'{self.resource} object up to date'

        return results

    def create(self, lobject):
        """Takes resource definition and returns dict containing http_code,
        changed and message.
        """
        results = {}
        self.pop_keys(lobject, self.ignore_keys['local'])

        if self.dryrun:
            results = {**results, **DRYRUN}
            results['changed'] = True
        else:
            create_object = self.create_resource(rdata=lobject)
            results['http_code'] = create_object.status_code
            results['message'] = json.loads(create_object.text).get('Messages')
            results['changed'] = create_object.status_code in [200, 201]

        results['diff'] = {'before': None, 'after': lobject}

        return results

    def create_or_update(self, rname, lobject):
        """Takes resource name and locally defined object and either creates a new
        resource or updates an existing one, if one exists
        """
        results = {}
        if self.exists(rname):
            results = {**results, **self.update(rname, lobject)}
        else:
            results = {**results, **self.create(lobject)}

        return results
