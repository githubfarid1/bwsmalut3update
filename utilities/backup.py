import tarfile
import os.path
from alihmedia_inactive.settings import *
import datetime
import glob
import uuid
FILE_COUNT = 14
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def main():
    files = glob.glob(os.path.join(BACKUP_LOCATION, "*.*"))
    latest_file = max(files, key=os.path.getctime)
    datenow = datetime.datetime.now().strftime("%Y%m%d")
    fname = "backup_{}.tar.gz".format(datenow)
    tmpname = "{}.tar.gz".format(str(uuid.uuid4()))
    make_tarfile(os.path.join(BACKUP_LOCATION, tmpname), PDF_LOCATION)
    if os.path.getsize(os.path.join(BACKUP_LOCATION, tmpname)) == os.path.getsize(latest_file):
        os.remove(os.path.join(BACKUP_LOCATION, tmpname))
    else:
        if os.path.exists(os.path.join(BACKUP_LOCATION, fname)):
            os.remove(os.path.join(BACKUP_LOCATION, fname))
        os.rename(os.path.join(BACKUP_LOCATION, tmpname), os.path.join(BACKUP_LOCATION, fname))

    files = glob.glob(os.path.join(BACKUP_LOCATION, "*.*"))
    if len(files) >= FILE_COUNT:
        oldest_file = min(files, key=os.path.getctime)
        os.remove(oldest_file)

if __name__ == '__main__':
    main()
