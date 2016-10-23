# coding=utf-8
from tickets.model import TicketModel, CommentModel, LikeModel


class TicketsDao(object):
    """

    """

    def __init__(self, db_connection):
        """

        :param db_connection:
        """
        self.dbConn = db_connection.get_connection(TicketModel)

    def create(self, ticketModel):
        """

        :param ticketModel:
        :return:
        """

        self.dbConn.insert(ticketModel.toDict())

    def getTicketById(self, ticket_id, user_id=None):
        """

        :param ticket_id:
        :param user_id:
        :return:
        """

        if user_id:
            query = {TicketModel.ID: ticket_id, TicketModel.USER_ID: user_id}
        else:
            query = {TicketModel.ID: ticket_id}

        result = self.dbConn.find_one(query)
        if result:
            return TicketModel.fromDict(result)

        return None

    def getMyTickets(self, user_id, limit=30, offset=0):
        """

        :param user_id:
        :param limit:
        :param offset:
        :return:
        """

        ticketList = self.dbConn.find({
            TicketModel.USER_ID: user_id
        }).sort(TicketModel.CREATED_DATE, -1).skip(offset).limit(limit)

        resp = [TicketModel.fromDict(ticket) for ticket in ticketList]

        return resp

    def incrementLike(self, ticket_id, value=1):
        """

        :param ticket_id:
        :return:
        """

        self.dbConn.update({TicketModel.ID: ticket_id}, {"$inc": {TicketModel.LIKES: value}})


class CommentsDao(object):
    """

    """

    def __init__(self, db_connection):
        """

        :param db_connection:
        """
        self.dbConn = db_connection.get_connection(CommentModel)

    def create(self, commentModel):
        """

        :param commentModel:
        :return:
        """

        data = commentModel.toDict()

        self.dbConn.insert(data)

    def getCommentsForTickets(self, ticketIds, user_id, limit=10):
        """
        get the last 10 comments for each ticket
        :param ticketIds:
        :param user_id:
        :param limit:
        :return:
        """

        respDict = dict((ticketId, []) for ticketId in ticketIds)

        # TODO find a better way to get the data, preferably in 1 go
        for ticketId in ticketIds:
            comments = self.dbConn.find({CommentModel.TICKET_ID: ticketId,
                                        CommentModel.USER_ID: user_id,
                                        CommentModel.HIDDEN: False}).sort(CommentModel.ID, -1).limit(limit)
            for comment in comments:
                respDict[ticketId].append(CommentModel.fromDict(comment))

        return respDict

class LikesDao(object):
    """

    """

    def __init__(self, db_connection):
        """

        :param db_connection:
        """
        self.dbConn = db_connection.get_connection(LikeModel)

    def getLikedByMe(self, ticketIds, user_id):
        """

        :param ticketIds:
        :param user_id:
        :return:
        """

        respDict = dict((ticketId, False) for ticketId in ticketIds)

        results = self.dbConn.find({LikeModel.TICKET_ID: {"$in": ticketIds}, LikeModel.USER_ID: user_id},
                         {LikeModel.ID: 0, LikeModel.TICKET_ID: 1})

        respDict.update(dict((ticketId.get(LikeModel.TICKET_ID), True) for ticketId in results))

        return respDict

    def getLike(self, ticket_id, user_id):
        """

        :param ticket_id:
        :param user_id:
        :return:
        """

        resp = self.dbConn.find_one({LikeModel.TICKET_ID: ticket_id, LikeModel.USER_ID: user_id})

        if resp:
            return LikeModel.fromDict(resp)

        return None

    def create(self, likeModel):
        """

        :param likeModel:
        :return:
        """

        data = likeModel.toDict()

        self.dbConn.insert(data)

    def deleteLike(self, like_id):
        """

        :param like_id:
        :return:
        """
        self.dbConn.remove({LikeModel.ID: like_id})