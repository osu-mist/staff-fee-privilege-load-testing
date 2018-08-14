Staff Fee Privilege API Load Testing
---

The purpose of this repo is to load balance the [Staff Fee Privilege API](https://github.com/osu-mist/staff-fee-privilege-api) using [Locust](https://github.com/locustio/locust).

## Usage

  1. Install all dependencies via pip:

      ```
      $ pip install -r requirements.txt
      ```

  2. Copy [config-example.yaml](config-example.yaml) as `config.yaml`. Modify as necessary, being careful to avoid committing sensitive data.

  3. Run API locally (e.g. https://localhost:8080) then start locust with Locust file:

      ```
      $ locust -f locustfile.py --host=https://localhost:8080
      ```

      Once you’ve started Locust, you should be able to open up a browser and point it to http://localhost:8089 to access Locust’s web interface.

## Report

The following report is generated with different amount of users.

| Concurrent Users | Total requests | Total Fails | Failures Percentage |
| ---------------- | -------------- | ----------- | ------------------- |
| 10 | 330 | 0 | 0% |
| 100 | 3665 | 28 | 1% |
| 500 | 3163 | 24 | 1% |
| 1000 | 3156 | 22 | 1% |
| 1500 | 3675 | 117 | 3% |
| 2000 | 2029 | 28 | 1% |
| 2000 | 2830 | 200 | 7% |
| 2000 | 3426 | 716 | 17% |

According to the report, all of the failures types are `ConnectionError(ProtocolError('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer')),)` and most of them occur on requesting the endpoints which need longer time to respond, e.g. `GET /api/v1/staff-fee-privilege?term=term_id` will take about 3 seconds to respond if not cached. The Staff Fee Privilege API handle requests pretty well when users are less than 1500, however, when users increase to more than 2000, the failures ratio start increasing obviously as well.
