import traceback

from flask import Response

ERRORS = {'REQUEST': ['Bad Request', 'Check that your request URL is valid and the authorisation given is valid.'],
          'BADID': ['Bad Request', 'The ID given did not return any results.'],
          'SERVER': ['Server Error', 'There was an issue with the server, please try again in a moment.'],
          'DATES': ['Date Order', 'Ensure that start dates are lower than end dates.'],
          'DATA': ['Bad Request', 'Check the data that you have given matches the requirements.'],
          'NOTFOUND': ['No Data', 'No data was found for the query given.'],
          'AUTH': ['Invalid Authorisation', 'The authorisation given was invalid'],
          'UNKNOWN': ['Unknown Error', 'An unknown error occurred.']
          }

def Get_error(etype='REQUEST', status=400):
    return Response('{"Error": "'+ERRORS[etype][0]+'", "Message": "'+ERRORS[etype][1]+'"}', status=status, mimetype='application/json')
