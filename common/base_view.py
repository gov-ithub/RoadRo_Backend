# coding=utf-8
import ujson
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, StreamingHttpResponse

class BaseView(View):
    """
        Handle a web view
    """

    CONTENT_JSON = "application/json"
    WWW_CONTENT = "application/x-www-form-urlencoded"

    def render_json_response(self, outData, statusCode=None, inHeaders=None):
        """
        render a json HTTP response
        :param outData: Base response or dictionary to convert in json
        :type outData: BaseResponse, dict
        :param inHeaders: dictionary to append http headers
        :type inHeaders: dic
        :param statusCode: http status code
        :type statusCode: int, str
        :param successCounter
        :param failCounter
        :return: Http Response
        :rtype: HttpResponse
        """

        serializedResp = ujson.dumps(outData)

        httpResp = HttpResponse(serializedResp)
        httpResp['Content-Length'] = len(serializedResp)
        httpResp['Content-Type'] = "application/json; charset=utf-8"
        if inHeaders is not None:
            for key in inHeaders.keys():
                httpResp[key] = inHeaders[key]

        httpResp.status_code = statusCode

        return httpResp

    def render_response(self, outData, statusCode=None, successCounter=None, failCounter=None):
        """
        render a json HTTP response
        :param outData: Base response or dictionary to convert in json
        :type outData: BaseResponse, dict
        :param statusCode: http status code
        :type statusCode: int, str
        :param successCounter
        :param failCounter
        :return: Http Response
        :rtype: HttpResponse
        """

        httpResp = HttpResponse(outData)
        httpResp['Content-Length'] = len(outData) if outData else 0
        httpResp['Content-Type'] = "application/json; charset=utf-8"

        httpResp.status_code = statusCode

        if successCounter and statusCode in (201, 200):
            successCounter.increment()

        if failCounter and statusCode not in (201, 200):
            failCounter.increment()

        return httpResp

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """
        overwritten
        """
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def render_file(self, path, mimetype):
        """

        :param path:
        :return:
        """
        f = open(path, "rb")
        try:
            content = f.read()
            httpResp = HttpResponse()
            httpResp.content = content
            httpResp["Content-Length"] = len(content)
            httpResp["Content-Type"] = mimetype
            httpResp.status_code = 200
            return httpResp
        except Exception as e:
            print(str(e))
            return HttpResponse(status=404)
        finally:
            if f and not f.closed:
                f.close()