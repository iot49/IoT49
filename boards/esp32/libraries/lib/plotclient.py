from json import dumps
import os

class PlotClient:

    def __init__(self, mqtt_client, session='iot49'):
        self.mqtt_client = mqtt_client
        self.session = session

    def new_series(self, *args):
        """create a new series on remote
        all data of a prior series with the same name will be lost
        arguments:
            series name (first)
            column names
        """
        self.__publish("new_series", args)

    def data(self, *args):
        """add data to series on remote, use after 'new_series'
        arguments:
            series name
            column values (same number as column names submitted with new_series)
        """
        self.__publish("data", args)

    def save_series(self, series, filename=None):
        """store series on remote in pickle format"""
        self.__publish("save_series", [ series, filename ])

    def plot_series(self, series, **kwargs):
        """plot series on remote"""
        self.__publish("plot_series", [ series, kwargs ])

    def __publish(self, topic, data):
        """send data to broker, do not call from other modules"""
        topic = os.path.join(self.session, topic)
        self.mqtt_client.publish(topic, dumps(data))
