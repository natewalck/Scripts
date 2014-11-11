#!/usr/bin/env python

import os
import twitter
import plistlib
import subprocess
import logging

app_versions = os.path.expanduser('~/Library/AutoPkg/app_versions.plist')
autopkg_report = os.path.expanduser('~/Library/AutoPkg/autopkg_report.plist')
recipe_list = os.path.expanduser('~/Library/AutoPkg/recipe_list.txt')
log_directory = os.path.expanduser('~/Library/AutoPkg/autopkg_tweeter.log')

twitter_account_name = 'autopkgsays'

logging.basicConfig(format='%(asctime)s %(message)s', filename=log_directory, level=logging.DEBUG)

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


def load_autopkg_results():
    if os.path.isfile(autopkg_report):
        report_data = plistlib.readPlist(autopkg_report)
    else:
        report_data = None

    return report_data


def get_previous_app_version(app_name):
    app_history = load_app_versions()
    if app_history and app_name in app_history:
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


def run_autopkg():
    cmd = ['/usr/local/bin/autopkg', 'run', '--recipe-list', recipe_list, '--report-plist=' + autopkg_report]
    string_cmd = " ".join(cmd)
    proc = subprocess.Popen(string_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, error_output) = proc.communicate()
    return output.strip()


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
    twitter_instance.statuses.update(status="%s %s has been released" % (app_name, version))


def tweet_if_new(app_name, version):
    previous_version = get_previous_app_version(app_name)

    if previous_version:
        if version > previous_version:
            logging.info("%s is newer than %s, saving version and sending tweet" % (app_name, version))
            store_app_version(app_name, version)
            try:
                tweet(app_name, version)
                logging.info("Tweeted %s has been updated to %s" % (env["app_name"], env["version"]))
            except:
                logging.info("Duplicate Tweet or Failed for another reason")
        else:
            logging.info("%s is not newer than %s" % (version, previous_version))
    else:
        logging.info("%s is newer than %s, saving version and sending tweet" % (app_name, version))
        store_app_version(app_name, version)
        try:
            tweet(app_name, version)
            logging.info("Tweeted %s has been updated to %s" % (env["app_name"], env["version"]))
        except:
            logging.info("Duplicate Tweet or Failed for another reason")

def main():
    logging.info("Running AutoPkg Tweeter...")
    autopkg_run_results = run_autopkg()
    autopkg_results = load_autopkg_results()
    autopkg_run = {}
    for item in autopkg_results['new_imports']:
        autopkg_run.update({item['name']:item['version']})

    for app in autopkg_run:
        tweet_if_new(app, autopkg_run[app])


if __name__ == "__main__":
    main()
