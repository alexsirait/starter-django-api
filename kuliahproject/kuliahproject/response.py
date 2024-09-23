from django.http import JsonResponse

class Response:
    def base(self, values=None, message="", messagetype="", status=200):
        if values is None:
            values = []

        return JsonResponse({
            'values': values,
            'message': message,
            'messagetype': messagetype,
        }, status=status)

    @staticmethod
    def ok(values=None, message="", messagetype=""):
        return Response().base(values=values, message=message, messagetype=messagetype, status=200)

    @staticmethod
    def badRequest(values=None, message="", messagetype=""):
        return Response().base(values=values, message=message, messagetype=messagetype, status=400)