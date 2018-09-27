#!/usr/bin/env python3

from enum import Enum, auto, unique


@unique
class HouseTopic(Enum):  # 房产话题
    GREET = auto()  # 问候话题
    PRICE = auto()  # 价格话题
    LOCATION = auto()  # 位置话题
    RESULT = auto()  # 结果话题


@unique
class HouseFeedback(Enum):  # 房产反馈
    ASK = auto()  # 主动询问
    POSITIVE = auto()  # 积极反馈
    NEGATIVE = auto()  # 消极反馈
    UNCLEAR = auto()  # 没听清


@unique
class HouseResult(Enum):
    CONTACT = auto()  # 用户请求联系方式
    APPOINT = auto()  # 用户主动邀约


@unique
class HouseAction(Enum):
    INTRO = auto()  # 主动介绍
    FIRST_REDEEM = auto()  # 第一轮挽回
    SECOND_REDEEM = auto()  # 第二轮挽回
    ANSWER = auto()  # 回答提问
    REPEAT = auto()  # 重复答案
    STOP = auto()  # 挂机停止


class HouseClassifier:
    '''Classifiers in house industry.
    '''

    @classmethod
    def class_topic(cls, text, prev_topic):
        '''Topic classification.

        Args:
            text (str): The classifing text.
            prev_topic (HouseTopic): The previous topic.

        Returns:
            Return a HouseTopic.
        '''
        if prev_topic == HouseTopic.GREET:
            return HouseTopic.GREET
        else:
            return HouseTopic[text.split()[0]]

    @classmethod
    def class_feedback(cls, text, topic):
        '''Feedback classification.

        Args:
            text (str): The classifing text.
            topic (HouseTopic): The topic of the text.

        Returns:
            Return a intent str.
        '''
        if topic is None:
            topic = cls.class_topic(text)
        text = text.split()[1]
        feedback_dict = {'N': HouseFeedback.NEGATIVE,
                         'Y': HouseFeedback.POSITIVE,
                         '?': HouseFeedback.UNCLEAR}
        return feedback_dict[text]
