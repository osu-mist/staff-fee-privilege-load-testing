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

The following report is generated with different amount of users and based on 30 connection pools.

| Concurrent Users | Total requests | Total Fails | Failures Percentage | Average (ms) | RPS |
| ---------------- | -------------- | ----------- | ------------------- | ------------ | --------- |
| 10 | 1012 | 0 | 0% | 140 | 3.3 |
| 20 | 1013 | 3 | 0% | 154 | 7.2 |
| 30 | 1524 | 3 | 0% | 172 | 10.5 |
| 50 | 2057 | 10 | 0% | 240 | 19.8 |
| 100 | 3695 | 33 | 1% | 417 | 34 |
| 500 | 4164 | 71 | 2% | 11953 | 38.3 |
| 1000 | 3706 | 53 | 1% | 29721 | 35.1 |
| 1500 | 2628 | 39 | 1% | 41294 | 32 |
| 1500 | 2936 | 151 | 5% | 40294 | 31.9 |
| 1500 | 3426 | 468 | 12% | 37388 | 27 |
| 2000 | 2015 | 23  | 1% | 45365 | 33.9 |
| 2000 | 2717 | 145 | 5% | 41892 | 38.8 |
| 2000 | 3128 | 847 | 21% | 39977 | 19.7 |

According to the report, all of the failures types are:

  * `ConnectionResetError(54, 'Connection reset by peer')`

  * `RemoteDisconnected('Remote end closed connection without response',)`

Due to the SQL query speed limit, most of these errors occurred on requesting the endpoints which need longer time to respond, for instance, `GET /api/v1/staff-fee-privilege?term=term_id` could take up to 3 seconds to respond if not cached. When users less than 100, the total connection pools consumed the requests pretty well and the API only took 417 ms in average to respond for 3695 requests.

However, when users grew to 500 - 1000, the speed performance started slowing down. This outcome was actually expected since we only have 30 pools for the load testing, and it seems like the limit of RPS (requests per second) of the API is 35 - 38, which means each pool could handle at most 1.1 - 1.2 requests per second when there are lots of users.

While total users increased to 1500 - 2000, not only the response average time was influenced, the failures percentage was affected as well. When total requests were less than about 2500, the API still have good failures percentage (around 1%), however, when total requests were increased to about 3000, the API couldn't handle that much requests and the failures rate started increase as well.
