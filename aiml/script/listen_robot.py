#!/usr/bin/env python3

import argparse
import os

import aiml
from aiml.script.house import HouseTopic
from aiml.script.house import HouseClassifier
from aiml.script.dialogue_state_tracking import DialogueStateTracking

'''This script define a demo of listen robot chatbot.
'''


def read_args():
    '''Read cmd-line arguments.
    '''
    parser = argparse.ArgumentParser(description='灵声机器人(Demo)',
                                     add_help=True)
    parser.add_argument('industry', type=str, nargs=1, help='行业')
    return parser.parse_args()


class ListenRobot:

    @property
    def current_topic(self):
        '''Current topic setter.

        Returns:
            Return a HouseTopic.
        '''
        return self._current_topic

    @current_topic.setter
    def current_topic(self, value):
        '''Current topic setter.

        Args:
            value (HouseTopic): The value to set.
        '''
        self.kernel.respond(f'EXEC SWITCH {value.name}')
        self._current_topic = value

    def __init__(self):
        '''Init the robot.

        Args:
            industry (str): The industry of the robot.
        '''
        avialable_industry_list = ('house',)
        args = read_args()
        industry = args.industry[0]

        if industry not in avialable_industry_list:
            raise ValueError(f'{industry}行业无法加载, 请检查您的配置文件.')
        self.kernel = aiml.Kernel()
        chdir = os.path.join(aiml.__path__[0], 'botdata', industry)
        self.kernel.bootstrap(learnFiles='startup.xml',
                              commands="LOAD LISTEN ROBOT", chdir=chdir)
        self._current_topic = None
        self.current_topic = HouseTopic.GREET
        self.dst = DialogueStateTracking()

    def output(self, text):
        '''Output text to the user.

        Args:
            text (str): The text to output.
        '''
        print('🤖 : ' + text)


    def user_update_str(self, user_input):
        '''Get user command str with feedback and topic.

        Args:
            user_input (str): Raw text of user input.

        Returns:
            Return a command str.
        '''
        user_topic = HouseClassifier.class_topic(user_input,
                                                 self.current_topic)
        user_feedback = HouseClassifier.class_feedback(user_input,
                                                       user_topic)
        user_str = f'FEEDBACK {user_topic.name} {user_feedback.name}'
        return user_str

    def run(self):
        '''Run the robot.
        '''
        print('-' * 80)
        print('欢迎使用灵声机器人 (输入ctrl-c退出)')
        print('-' * 80)
        try:
            robot_action = 'ACTION GREET INTRO'
            action_text = self.kernel.respond(robot_action)
            self.output(action_text)
            self.dst.update(robot_action, action_text)
            while True:
                user_input = input('📞 : ')
                if user_input == 'PRINT':
                    print(self.dst)
                    continue
                user_str = self.user_update_str(user_input)
                self.dst.update(user_str, user_input)
                feedback_topic_str = user_str.split()[1]
                if feedback_topic_str != self.current_topic.name:
                    self.current_topic = HouseTopic[feedback_topic_str]
                feedback_cmd_str = user_str.split()[2]
                if feedback_cmd_str == 'UNCLEAR':
                    self.dst.update(robot_action, action_text, repeat=True)
                    self.output(action_text)
                    continue
                robot_action = self.kernel.respond(user_str)
                _, action_topic_str, action_cmd = robot_action.split()
                if action_topic_str != self.current_topic.name:
                    self.current_topic = HouseTopic[action_topic_str]
                action_text = self.kernel.respond(robot_action)
                self.dst.update(robot_action, action_text)
                self.output(action_text)
                if action_cmd == 'STOP':
                    break
        except KeyboardInterrupt:
            print('Interrupted!')
        except EOFError:
            print('Terminated!')


if __name__ == '__main__':
    robot = ListenRobot()
    robot.run()
