#!/usr/bin/env python

import os
import twitter
import plistlib

app_versions = os.path.expanduser('~/Library/AutoPkg/app_versions.plist')
twitter_account_name = 'autopkgsays'


def load_app_keys():
    """Load app keys from a file on disk"""
    twitter_app_keys_path = os.path.expanduser('~/.twitter_app_keys')
    with open (twitter_app_keys_path) as f:
        credentials = [x.strip().split(':') for x in f.readlines()]

    return credentials[0]


def load_app_versions():
    if os.path.isfile(app_versions):
        versions = plistlib.readPlist(app_versions)
    else:
        versions = None

    return versions


def get_previous_app_version(app_name):
    app_history = load_app_versions()
    if app_history and app_history[app_name]:
        return app_history[app_name]
    else:
        return False


def store_app_version(app_name, version):
    app_history = load_app_versions()
    if app_history:
        app_history.update({app_name: version})
        plistlib.writePlist(app_history, app_versions)
    else:
        app_history = {app_name: version}
        plistlib.writePlist(app_history, app_versions)


def tweet(app_name, version):
    MY_TWITTER_CREDS = os.path.expanduser('~/.twitter_oauth')
    CONSUMER_KEY, CONSUMER_SECRET = load_app_keys()

    if not os.path.exists(MY_TWITTER_CREDS):
        twitter.oauth_dance(twitter_account_name, CONSUMER_KEY, CONSUMER_SECRET,
                    MY_TWITTER_CREDS)
    oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)
    twitter_instance = twitter.Twitter(auth=twitter.OAuth(
        oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
    # Now work with Twitter
    twitter_instance.statuses.update(status="%s version %s has been released" % (app_name, version))

def main():
    app_name = env["app_name"]
    version = env["version"]

    previous_version = get_previous_app_version(app_name)

    if previous_version:
        if version > previous_version:
            output("%s is newer than %s, saving version and sending tweet" % (app_name, version))
            store_app_version(app_name, version)
            try:
                tweet(app_name, version)
                output("Tweeted %s has been updated to %s" % (env["app_name"], env["version"]))
            except:
                output("Duplicate Tweet or Failed for another reason")
        else:
            output("%s is not newer than %s" % (version, previous_version))
    else:
        output("%s is newer than %s, saving version and sending tweet" % (app_name, version))
        store_app_version(app_name, version)
        try:
            tweet(app_name, version)
            output("Tweeted %s has been updated to %s" % (env["app_name"], env["version"]))
        except:
            output("Duplicate Tweet or Failed for another reason")


if __name__ == "__main__":
    main()
