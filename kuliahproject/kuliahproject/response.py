from django.http import JsonResponse

class Response:
    def base(self, data=None, message="", messagetype="", status=200):
        if data is None:
            data = []

        return JsonResponse({
            'status_code': status,
            'message': message,
            'messagetype': messagetype,
            'data': data,
        }, status=status)

    @staticmethod
    def ok(data=None, message="", messagetype=""):
        return Response().base(data=data, message=message, messagetype=messagetype, status=200)

    @staticmethod
    def badRequest(data=None, message="", messagetype=""):
        return Response().base(data=data, message=message, messagetype=messagetype, status=400)