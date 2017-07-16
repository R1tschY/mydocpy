# -*- coding=utf-8 -*-


class ServiceLocator(object):
    """
    :ivar services: list with services
    :type services: dict(type: object)
    """

    def __init__(self):
        self.services = []

    def register(self, service):
        """
        :param service: Service
        :type service: object
        """
        self.services[type(service)] = service

    def get(self, serviceType):
        """
        :param serviceType: Type of requested service
        :type serviceType: type

        :return: Service with type ``serviceType``
        :rtype: object
        """
        return self.services[serviceType]
