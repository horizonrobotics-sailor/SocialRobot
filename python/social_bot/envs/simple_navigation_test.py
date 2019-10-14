# Copyright (c) 2019 Horizon Robotics. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import multiprocessing
from multiprocessing import Process, Value
from simple_navigation import SimpleNavigationLanguage
import random
import os


class Agent(Process):
    def __init__(self, agent_id):
        super(Agent, self).__init__()
        self.ok = Value('i', 0)
        self.agent_id = agent_id

    def run(self):
        port = os.environ.get('PYGAZEBO_PORT', 11345)
        env = SimpleNavigationLanguage(port=port + self.agent_id + 1)
        env.reset()
        for _ in range(1000):
            control = [
                random.random() * 0.2 - 0.1,
                random.random() * 0.2 - 0.1
            ]
            obs, reward, done, info = env.step(
                dict(control=control, sentence="hello"))
            if done:
                env.reset()
        self.ok.value = 1


class TestMultiProcess(unittest.TestCase):
    def test_multiprocessing(self):
        env = SimpleNavigationLanguage()
        env.reset()
        agents = [Agent(i) for i in range(2)]
        for agent in agents:
            agent.start()
        for agent in agents:
            agent.join()
        for agent in agents:
            self.assertTrue(agent.ok.value)


if __name__ == '__main__':
    # we use spawn to make sure pygazebo has a clean state in each subprocess
    multiprocessing.set_start_method('spawn')
    unittest.main()
