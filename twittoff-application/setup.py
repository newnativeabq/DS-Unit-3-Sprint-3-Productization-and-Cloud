import os


def setup_environment():
    # os.environ['var_name'] = var_value
    os.environ['SECRET_KEY'] = 'dev'
    os.environ['TWITTER_CONSUMER_KEY'] = "iXUo5K45Do37vqh9G2A5Ahmty"
    os.environ['TWITTER_CONSUMER_SECRET'] = "nDWJgxYlpQwKm2sjz6GExRRD3exmcgUaIQzH7Sf5xa17SHt5GG"
    os.environ['TWITTER_ACCESS_TOKEN'] = "489867967-5B4D9l8s0MZkSMUgJ9vC70NOnZG624ZABrXyiIqd"
    os.environ['TWITTER_ACCESS_TOKEN_SECRET'] = "Rfae5VKnGVOP5O3qAZgOB2VqBIvfSGBVYPRXT45hjszvZ"
    os.environ['BASILICA_ACCESS_TOKEN'] = "2c506c0c-dc0b-a0ab-a7ea-202b1f3f5df1"


if __name__ == "__main__":
    pass