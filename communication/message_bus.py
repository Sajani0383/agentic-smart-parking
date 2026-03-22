from collections import defaultdict


class MessageBus:

    def __init__(self):

        self.subscribers = defaultdict(list)

        self.messages = []

    def subscribe(self, topic, agent):

        self.subscribers[topic].append(agent)

    def publish(self, topic, message):

        self.messages.append((topic, message))

        if topic in self.subscribers:

            for agent in self.subscribers[topic]:

                agent.receive(topic, message)

    def get_messages(self):

        return self.messages