# coding=utf-8
from common.base_view import BaseView
from bson.objectid import ObjectId

# Create your views here.

class ImgServeView(BaseView):

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        img_id = kwargs["img_id"]
        if "_" in img_id:
            index = img_id.find('_')
            dbId = img_id[index+1:]
        else:
            dbId = img_id
        imgDict = request.ticketService.dbConn.get_connection("images").find_one({"_id": ObjectId(dbId)})
        path = "%s%s/%s/%s" % (request.ticketService.base_img_path, img_id[-2:], img_id[-4:-2], img_id)
        return self.render_file(path, imgDict["mimetype"])