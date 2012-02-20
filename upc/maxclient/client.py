import requests
import json
from upc.maxclient import ROUTES


class MaxClient(object):

    def __init__(self, url, actor=None):
        """
        """
        self.url = url
        self.setActor(actor)

    def setActor(self, displayName):
        self.actor = self.actor and dict(objectType='person', displayName=displayName) or None

    def GET(self, route, query=None):
        """
        """
        resource_uri = '%s/%s' % (self.url, route)
        req = requests.get(resource_uri)

        isOk = req.status_code == 200
        isJson = 'application/json' in req.headers.get('content-type', '')
        if isOk:
            response = isJson and json.loads(req.content) or None
        else:
            print req.status_code
            response = ''
        return (isOk, req.status_code, response)

    def POST(self, route, query):
        """
        """
        resource_uri = '%s/%s' % (self.url, route)
        json_query = json.dumps(query)

        req = requests.post(resource_uri, data=json_query)
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

    def addUser(self, displayName):
        """
        """
        route = ROUTES['user']

        query = {}
        rest_params = dict(displayName=displayName)

        (success, code, response) = self.POST(route % (rest_params), query)
        return response

    ###########################
    # ACTIVITIES
    ###########################

    def addActivity(self, content, otype='note', contexts=[]):
        """
        """
        route = ROUTES['user_activities']
        query = dict(verb='post',
                     object=dict(objectType=otype,
                                   content=content,
                                  ),
                    )
        if contexts:
            query['contexts'] = contexts

        rest_params = dict(displayName=self.actor['displayName'])

        (success, code, response) = self.POST(route % rest_params, query)
        return response

    def getActivity(self, activity):
        """
        """
        route = ROUTES['activity']
        rest_params = dict(activity=activity)
        (success, code, response) = self.GET(route % rest_params)
        return response

    def getUserTimeline(self, displayName):
        """
        """
        route = ROUTES['timeline']
        rest_params = dict(displayName=displayName)
        (success, code, response) = self.GET(route % rest_params)
        return response

    ###########################
    # COMMENTS
    ###########################

    def addComment(self, content, activity, otype='comment'):
        """
        """
        route = ROUTES['comments']
        query = dict(actor=self.actor,
                     verb='post',
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

    def examplePOSTCall(self, displayName):
        """
        """
        route = ROUTES['']

        query = {}
        rest_params = dict(displayName=displayName)

        (success, code, response) = self.POST(route % rest_params, query)
        return response

    def exampleGETCall(self, param1, param2):
        """
        """
        route = ROUTES['']
        rest_params = dict(Param1=param1)
        (success, code, response) = self.GET(route % rest_params)
        return response

    # def follow(self,displayName,oid,otype='person'):
    #     """
    #     """

    # def unfollow(self,displayName,oid,otype='person'):
    #     """
    #     """

    # def subscribe(self,url,otype='context'):
    #     """
    #     """

    # def unsubscribe(self,displayName,url,otype='service'):
    #     """
    #     """
