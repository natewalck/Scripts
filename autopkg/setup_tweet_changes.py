#!/usr/bin/env python

import os
import twitter

account_name = 'autopkgsays'

def load_app_keys():
    """Load app keys from a file on disk"""
    twitter_app_keys_path = os.path.expanduser('~/.twitter_app_keys')
    with open (twitter_app_keys_path) as f:
        credentials = [x.strip().split(':') for x in f.readlines()]

    return credentials[0]


def setup_twitter_oauth(CONSUMER_KEY, CONSUMER_SECRET):
    MY_TWITTER_CREDS = os.path.expanduser('~/.twitter_oauth')

    if not os.path.exists(MY_TWITTER_CREDS):
        twitter.oauth_dance(account_name, CONSUMER_KEY, CONSUMER_SECRET,
                    MY_TWITTER_CREDS)
    oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

def main():
    CONSUMER_KEY, CONSUMER_SECRET = load_app_keys()
    setup_twitter_oauth(CONSUMER_KEY, CONSUMER_SECRET)


if __name__ == "__main__":
    main()