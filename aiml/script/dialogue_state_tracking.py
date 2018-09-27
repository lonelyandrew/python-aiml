#!/usr/bin/env python3

'''DialogueStateTracking (DST) records some useful states during the dialogue.
'''

from aiml.script.house import HouseFeedback
from aiml.script.house import HouseTopic


class DialogueStateTracking:

    def __init__(self):
        # 通用状态, 用户和机器人均会更新
        self.nturns = 0  # 对话轮数
        self.mentioned_topic_set = set()  # 提及的话题
        self.text_history_list = []  # 对话文本记录
        self.topic_history_list = []  # 话题记录

        # 用户状态, 只有用户可以更新
        self.feedback_dict = {}  # 用户对于话题的反馈
        self.feedback_history_list = []  # 用户反馈记录

        # 机器人状态, 只有机器人可以更新
        self.redeem_dict = {}  # 各个话题的挽回次数
        self.action_history_list = []  # 机器人操作记录


    def __str__(self):
        state_str = f'#TURNS: {self.nturns}\n'
        state_str += f'MENTIONED TOPICS: {self.mentioned_topic_set}\n'
        state_str += f'TEXT HISTORY: {self.text_history_list}\n'
        state_str += f'TOPIC HISTORY: {self.topic_history_list}\n'
        state_str += f'FEEDBACK OF TOPICS: {self.feedback_dict}\n'
        state_str += f'FEEDBACK HISTORY: {self.feedback_history_list}\n'
        state_str += f'REDEEM OF TOPICS: {self.redeem_dict}\n'
        state_str += f'ACTION HISTORY LIST: {self.action_history_list}\n'
        return state_str

    def update(self, update_str, text, repeat=False):
        '''Update the states.

        Args:
            update_str(str): The command str.
            text (str): The conversation text.
        '''
        cmd_type, topic_str, cmd_str = update_str.split()
        if cmd_type == 'ACTION':
            self.nturns += 1
            role = 'ROBOT'
        else:
            role = 'USER'
        topic = HouseTopic[topic_str]
        if topic.name not in self.mentioned_topic_set:
            self.mentioned_topic_set.add(topic.name)
        self.text_history_list.append({role: text})
        self.topic_history_list.append({role: topic.name})

        if role == 'USER':
            feedback = HouseFeedback[cmd_str]
            if feedback in (HouseFeedback.NEGATIVE, HouseFeedback.POSITIVE):
                self.feedback_dict[topic.name] = feedback.name
            self.feedback_history_list.append(update_str)
        elif role == 'ROBOT':
            if cmd_str == 'REDEEM' and not repeat:
                self.redeem_dict[topic.name] = self.redeem_dict.get(topic.name,
                                                                    0) + 1
            self.action_history_list.append(update_str)
