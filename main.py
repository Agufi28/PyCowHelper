import argparse
import requests

def changeMaxSyncedEmailAge(options):
    jobs = requests.get(f"http://{options['server']}/api/v1/get/syncjobs/all/no_log",headers={'X-API-Key':options['api_key']})
    print(jobs.text)

availableFunctions = {
    'changeMaxEmailAgeForSyncJobs': changeMaxSyncedEmailAge
}

def main(argv):
    if argv["api_key"] is None:
        argv["api_key"] = input("MAilCow API KEY: ")
    if argv["server"] is None:
        argv["server"] = input("MailCow server (IP:PORT or FQDN): ")

    availableFunctions[argv['action']](argv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Python helper for MailCow automations")

    availableOptionsHelp = '''
        changeMaxEmailAgeForSyncJobs => Sets a new max age for the emails fetched while syncing. By default this only affects previously ran jobs. If the [--max-age] flag is not set it will diable the max age limitation for all jobs.
    '''

    parser.add_argument('-k','--api-key', help="API Key for the targeted MailCow instance.")
    parser.add_argument('-s','--server', help="IP:Port of FQDN of targeted MailCow.")
    parser.add_argument('-a','--action', required=True, help=f"Tarea a realizar:\n {availableOptionsHelp}")
    parser.add_argument('--max-age', help="Max age allowed for the synced emails.")
    parser.add_argument('--domain', help="Targeted domain within the MailCow server.")
    parser.add_argument('--target-new-jobs', help="Ignores the default restriction for updating SyncJobs of only modifying previously ran jobs.")
    parser.add_argument('--target-disabled-jobs', help="Ignores the default restriction for updating SyncJobs of only active jobs.")
    

    main(vars(parser.parse_args()))