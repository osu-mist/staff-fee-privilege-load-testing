import random
import yaml
import urllib3
from locust import HttpLocust, TaskSet, task


# Load config file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
with open('config.yaml', 'r') as config_file:
    try:
        config = yaml.load(config_file)
        api_base_url = config['api_base_url']
        auth = (config['user'], config['password'])
    except yaml.YAMLError as error:
        exit(error)

term_ids = [f'20{y:02}0{t}' for y in range(15, 20) for t in range(0, 4)]
osu_ids = set()


class UserBehavior(TaskSet):
    # get some ids before run the task set
    def on_start(self):
        self.get_by_term_id()

    @task(2)
    def get_by_osuId_id(self):
        osu_id = random.sample(osu_ids, 1)[0]
        url = f'{api_base_url}?osuId={osu_id}'
        self.client.get(url, verify=False, auth=auth)

    @task(2)
    def get_by_term_id(self):
        term_id = random.choice(term_ids)
        url = f'{api_base_url}?term={term_id}'
        with self.client.get(
            url,
            catch_response=True, verify=False, auth=auth
        ) as response:
            if response.status_code == 200:
                if response.json()['data'] and len(osu_ids) < 10:
                    data = random.choice(response.json()['data'])
                    osu_ids.add(data['id'][:9])
                response.success()

    @task(1)
    def get_by_bad_request(self):
        url = f'{api_base_url}'
        with self.client.get(
            url,
            catch_response=True, verify=False, auth=auth
        ) as response:
            if response.status_code == 400:
                response.success()

    @task(1)
    def get_by_id(self):
        term_id = random.choice(term_ids)
        osu_id = random.sample(osu_ids, 1)[0]
        url = f'{api_base_url}/{osu_id}-{term_id}'
        with self.client.get(
            url,
            catch_response=True, verify=False, auth=auth
        ) as response:
            if response.status_code == 200 or response.status_code == 404:
                response.success()


class ApiUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 5000
