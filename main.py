import argparse
import requests
from loguru import logger
import sys
import json 

logger.remove()
logger.add("PyCowHelper_{time}.log",rotation="w6",format="{time:DD/MM/YYYY HH:mm:ss} - {level} - {message}")
logger.add(sys.stdout, colorize=True, format="<level>{time:DD/MM/YYYY HH:mm:ss} - {level} - {message}</level>")


def massSyncjobEdit(options):
    jobs = requests.get(f"http://{options['server']}/api/v1/get/syncjobs/all/no_log",headers={'X-API-Key':options['api_key']})
    
    if jobs.status_code != 200:
        logger.error(f"{options['action']} - Error obteniendo los syncjobs - Response text: {jobs.text}")
        return
    
    for job in json.loads(jobs.text):
        if options['domain'] != None and job['user2'].split("@")[1] != options['domain']:
            logger.info(f"Salteando syncjob[{job['id']}] para cuenta [{job['user2']}] correspondiente correspondiente a otro dominio")
            continue

        if not options['target_new_jobs'] and job['last_run'] == None:
            logger.info(f"Salteando syncjob[{job['id']}] nuevo")
            continue

        if not options['target_disabled_jobs'] and job['active'] == 0:
            logger.info(f"Salteando syncjob[{job['id']}] desactivado")
            continue

        

availableFunctions = {
    'massSyncJobEdit': massSyncjobEdit
}

def main(argv):
    print(argv)
    if argv["api_key"] is None:
        argv["api_key"] = input("MAilCow API KEY: ")
    if argv["server"] is None:
        argv["server"] = input("MailCow server (IP:PORT or FQDN): ")


    availableFunctions[argv['action']](argv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Python helper for MailCow automations")

    availableOptionsHelp = '''
        massSyncJobEdit => Massively edits the targeted syncjobs on a mailcow server.
    '''

    parser.add_argument('-k','--api-key', help="API Key for the targeted MailCow instance.")
    parser.add_argument('-s','--server', help="IP:Port of FQDN of targeted MailCow.")
    parser.add_argument('-a','--action', required=True, help=f"Tarea a realizar:\n {availableOptionsHelp}")
    parser.add_argument('--domain', help="Targeted domain within the MailCow server.")
    parser.add_argument('--max-age', help="Max age allowed for the synced emails.")
    parser.add_argument('--remote-host', help="Remote host used for syncing the targeted accounts.")
    parser.add_argument('--remote-port', help="Remote port used for syncing the targeted accounts.")
    
    parser.add_argument('--exclude', help="Exclude configuration for syncing the accounts.")
    parser.add_argument('--activation-status', help="Set all targeted syncjobs active/disabled.")
    parser.add_argument('--target-new-jobs', action='store_true', help="Ignores the default restriction for updating SyncJobs of only modifying previously ran jobs.")
    parser.add_argument('--target-disabled-jobs', action='store_true', help="Ignores the default restriction for updating SyncJobs of only active jobs.")
    

    main(vars(parser.parse_args())) 