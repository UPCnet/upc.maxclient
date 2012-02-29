import requests
import json
import urllib
from upc.maxclient import ROUTES


class MaxClient(object):

    def __init__(self, url, actor=None, auth_method='basic'):
        """
        """
        #Strip ending slashes, as all routes begin with a slash
        self.url = url.rstrip('/')
        self.setActor(actor)
        self.auth_method = auth_method

    def setActor(self, actor, type='person'):
        self.actor = actor and dict(objectType='person', username=actor) or None

    def setOAuth2Auth(self, oauth2_token, oauth2_grant_type='password', oauth2_scope='pythoncli'):
        """
        """
        self.token = oauth2_token
        self.grant = oauth2_grant_type
        self.scope = oauth2_scope

    def setBasicAuth(self, username, password):
        """
        """
        self.ba_username = username
        self.ba_password = password

    def OAuth2AuthHeaders(self):
        """
        """
        headers = {
            'X-Oauth-Token': self.token,
            'X-Oauth-Username': self.actor['username'],
            'X-Oauth-Scope': self.scope,
        }
        return headers

    def BasicAuthHeaders(self):
        """
        """
        auth = (self.ba_username, self.ba_password)
        return auth

    def GET(self, route, qs=''):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        if qs:
            resource_uri = '%s?%s' % (resource_uri, qs)
        if self.auth_method == 'oauth2':
            headers.update(self.OAuth2AuthHeaders())
            req = requests.get(resource_uri, headers=headers, verify=False)
        elif self.auth_method == 'basic':
            req = requests.get(resource_uri, auth=self.BasicAuthHeaders(), verify=False)
        else:
            raise

        isOk = req.status_code == 200
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = isJson and json.loads(req.content) or None
        else:
            print req.status_code
            response = ''
        return (isOk, req.status_code, response)

    def POST(self, route, query={}):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        json_query = json.dumps(query)

        if self.auth_method == 'oauth2':
            headers.update(self.OAuth2AuthHeaders())
            headers.update({'content-type': 'application/json'})
            req = requests.post(resource_uri, data=json_query, headers=headers, verify=False)
        elif self.auth_method == 'basic':
            req = requests.post(resource_uri, data=json_query, auth=self.BasicAuthHeaders(), verify=False)
        else:
            raise

        isOk = req.status_code in [200, 201] and req.status_code or False
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = isJson and json.loads(req.content) or None
        else:
            print req.status_code
            response = ''

        return (isOk, req.status_code, response)

    def PUT(self, route, query={}):
        """
        """
        headers = {}
        resource_uri = '%s%s' % (self.url, route)
        json_query = json.dumps(query)

        if self.auth_method == 'oauth2':
            headers.update(self.OAuth2AuthHeaders())
            req = requests.put(resource_uri, data=json_query, headers=headers, verify=False)
        elif self.auth_method == 'basic':
            req = requests.put(resource_uri, data=json_query, auth=self.BasicAuthHeaders(), verify=False)
        else:
            raise

        isOk = req.status_code in [200, 201] and req.status_code or False
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = isJson and json.loads(req.content) or None
        else:
            print req.status_code
            response = ''

        return (isOk, req.status_code, response)

    ###########################
    # USERS
    ###########################

    def addUser(self, username, **kwargs):
        """
        """
        route = ROUTES['user']

        query = {}
        rest_params = dict(username=username)
        valid_properties = ['displayName']
        query = dict([(k, v) for k, v in kwargs.items() if k in valid_properties])

        (success, code, response) = self.POST(route % (rest_params), query)
        return response

    def modifyUser(self, username, properties):
        """
        """
        route = ROUTES['user']

        query = properties
        rest_params = dict(username=username)
        import ipdb; ipdb.set_trace( )
        (success, code, response) = self.PUT(route % (rest_params), query)
        return response

    ###########################
    # ACTIVITIES
    ###########################

    def addActivity(self, content, otype='note', contexts=[]):
        """
        """
        route = ROUTES['user_activities']
        query = dict(object=dict(objectType=otype,
                                   content=content,
                                  ),
                    )
        if contexts:
            query['contexts'] = contexts

        rest_params = dict(username=self.actor['username'])

        (success, code, response) = self.POST(route % rest_params, query)
        return response

    def getActivity(self, activity):
        """
        """
        route = ROUTES['activity']
        rest_params = dict(activity=activity)
        (success, code, response) = self.GET(route % rest_params)
        return response

    def getUserTimeline(self):
        """
        """
        route = ROUTES['timeline']
        rest_params = dict(username=self.actor['username'])
        (success, code, response) = self.GET(route % rest_params)
        return response

    def getUserActivities(self, contexts=[]):
        """
        """
        route = ROUTES['activities']
        query = {}
        if contexts:
            query = {'contexts': contexts}
        (success, code, response) = self.GET(route, qs=urllib.urlencode(query, True))
        return response

    ###########################
    # COMMENTS
    ###########################

    def addComment(self, content, activity, otype='comment'):
        """
        """
        route = ROUTES['comments']
        query = dict(actor=self.actor,
                     object=dict(objectType=otype,
                                 content=content,
                                  ),
                    )
        rest_params = dict(activity=activity)
        (success, code, response) = self.POST(route % rest_params, query)
        return response

    def getComments(self, activity):
        """
        """
        route = ROUTES['comments']
        rest_params = dict(activity=activity)
        (success, code, response) = self.GET(route % rest_params)

    ###########################
    # SUBSCRIPTIONS
    ###########################

    def subscribe(self, url, otype='context'):
        """
        """
        route = ROUTES['subscriptions']

        query = dict(object=dict(objectType=otype,
                                 url=url,
                                  ),
                    )
        rest_params = dict(username=self.actor['username'])

        (success, code, response) = self.POST(route % rest_params, query)
        return response

    # def unsubscribe(self,username,url,otype='service'):
    #     """
    #     """

    def examplePOSTCall(self, username):
        """
        """
        route = ROUTES['']

        query = {}
        rest_params = dict(username=username)

        (success, code, response) = self.POST(route % rest_params, query)
        return response

    def exampleGETCall(self, param1, param2):
        """
        """
        route = ROUTES['']
        rest_params = dict(Param1=param1)
        (success, code, response) = self.GET(route % rest_params)
        return response

    # def follow(self,username,oid,otype='person'):
    #     """
    #     """

    # def unfollow(self,username,oid,otype='person'):
    #     """
    #     """
