# -*- coding: utf-8 -*-
"""
    Cryptography module
"""
__author__ = 'bogdan'

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
import logging
import random
from roadro import settings as projSettings


logger = logging.getLogger(__name__)


class Cryptography(object):
    """
    class that will have static methods to encrypt and decrypt
    """
    AES_PASSWD = projSettings.SECRET_KEY[:32]

    @classmethod
    def padPkcs7(cls, message):
        """
        added padding at the end of the message to make it's length multiple of 8
        :param cls:
        :param message: original message
        :return: padded message
        """
        length = 16 - (len(message) % 16)
        data = message + bytes([length]) * length

        return data

    @classmethod
    def encryptAES_CFB(cls, message):
        """
        encrypts the message with AES_CFB encryption algorithm
        :param message: the message to be encrypted
        :return: the encrypted message in hexadecimal format
        :rtype string
        """

        paddedMessage = cls.padPkcs7(message)
        iv = bytes([random.randint(0, 255) for _ in range(AES.block_size)])
        temp = base64.b64encode(iv +
            AES.new(
                cls.AES_PASSWD,
                AES.MODE_CFB,
                iv).encrypt(paddedMessage))
        temp = temp.decode().replace('+', '-').replace('/', '_')
        return temp

    @classmethod
    def encryptListAES_CFB(cls, messageList):
        """
        encrypts the message with AES CFB encryption algorithm
        :param messageList: the list of messages to be encrypted
        :return: the encrypted message list in hexadecimal format
        :rtype list
        """

        encryptedMessageList = []
        for message in messageList:
            paddedMessage = cls.padPkcs7(message.encode())

            iv = bytes([random.randint(0, 255) for _ in range(AES.block_size)])
            temp = base64.b64encode(iv +
                                    AES.new(cls.AES_PASSWD,
                                            AES.MODE_CFB,
                                            iv).encrypt(paddedMessage)).decode()
            temp = temp.replace('+', '-').replace('/', '_')

            encryptedMessageList.append(temp)
        return encryptedMessageList

    @classmethod
    def decryptAES_CFB(cls, encryptedText):
        """
        decrypts the received text using
        :param encryptedText: the text do be decrypted
        :return: the original message
        :rtype str, unicode
        """
        encryptedText = encryptedText.replace('-', '+').replace('_', '/')
        temp = base64.b64decode(encryptedText.encode())
        iv = bytes([random.randint(0, 255) for _ in range(AES.block_size)])
        deciphered = AES.new(cls.AES_PASSWD, AES.MODE_CFB, iv).decrypt(temp)
        return deciphered[16:-1*deciphered[-1]].decode()

    @classmethod
    def decryptList(cls, encryptedTextList):
        """
        handles matching of algorithm and decryption using the correct key and algo
        :param cls:
        :param encryptedTextList: List of XX_ciphered_text, where XX is the code for the algorithm to be used for decryption
        :return: List of original messages
        :rtype list
        """

        originalMessageList = []
        for encryptedText in encryptedTextList:
            originalMessageList.append(cls.decryptAES_CFB(encryptedText))

        return originalMessageList

    @classmethod
    def hash(cls, text):
        """

        :param text:
        :return:
        """
        ret = SHA256.new()
        ret.update(text.encode())
        return ret.hexdigest()
