#!/usr/bin/python
from datetime import datetime
from os import chdir, remove
from subprocess import call

from cloudfiles import get_connection

# Don't commit the real API_KEY!
API_KEY = 'Not a real API KEY'

def backup_database():
    # First, generate the filename we will be using from the current time in UTC
    timestamp = datetime.utcnow().isoformat()
    timestamp = timestamp.replace(':', '-')
    chdir('/tmp')
    filename = 'newdjangosite-prod-db-{0}.dump'.format(timestamp)
    file = open(filename, 'wb')

    # Now create the backup
    call(['pg_dump', '--format=custom', 'newdjangosite_prod'], stdout=file)
    file.close()

    # Now connection to Cloud Files
    connection = get_connection(username='newdjangosite_rackspace_user', api_key=API_KEY, servicenet=True)
    backup_container = connection.get_container('database-backups')

    # Now upload the new backup
    current_backup = backup_container.create_object(filename)
    current_backup.load_from_filename(filename)

    # Now delete the backup file we created locally
    remove(filename)

    # Now prune the backups if needed
    backup_objects = backup_container.get_objects()
    while len(backup_objects) > 168: # Keep one backup an hour for a week (168 = 24 * 7)
        # We have too many backups, delete the oldest one.
        # The oldest one has a file name that is less than all other objects.
        oldest = backup_objects[0].name
        for object in backup_objects:
            if object.name < oldest:
                oldest = object

        backup_container.delete_object(oldest)
        backup_objects = backup_container.get_objects()

if __name__ == "__main__":
    backup_database()

