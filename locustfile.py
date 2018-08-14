import yaml
import urllib3
from locust import HttpLocust, TaskSet, task


# Load config file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
with open('config.yaml', 'r') as config_file:
    try:
        config = yaml.load(config_file)
        api_base_url = config['api_base_url']
        term_id = config['term_id']
        osu_id = config['osu_id']
        auth = (config['user'], config['password'])
    except yaml.YAMLError as error:
        exit(error)


class UserBehavior(TaskSet):
    @task(2)
    def get_by_osuId_id(self):
        url = '{}?osuId={}'.format(api_base_url, osu_id)
        self.client.get(url, verify=False, auth=auth)

    @task(3)
    def get_by_term_id(self):
        url = '{}?term={}'.format(api_base_url, term_id)
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_by_bad_request(self):
        url = '{}'.format(api_base_url)
        with self.client.get(
            url,
            catch_response=True, verify=False, auth=auth
        ) as response:
            if response.status_code == 400:
                response.success()

    @task(2)
    def get_by_id(self):
        url = '{}/{}'.format(api_base_url, '{}-{}'.format(osu_id, term_id))
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_by_bad_id(self):
        url = '{}/{}'.format(api_base_url, 'invalid_id')
        with self.client.get(
            url,
            catch_response=True, verify=False, auth=auth
        ) as response:
            if response.status_code == 404:
                response.success()


class ApiUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 5000
