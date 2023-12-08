What to do when you have  root dir that is causing issues?

I found this online on stackoverflow


First standard cleanup & update.

sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
sudo apt-get autoclean

Autoclean cleans up the downloaded archives (.gz or .tar) files used to install things. Autoremove cleans libraries that are no longer needed.

Then we can start search for large folders with du.

Size of apt caches (often an issue)

sudo du -sh /var/cache/apt/archives

find ~/.cache/ -depth -type f -atime +90 

Delete all old cache entries, you can change to any number of days.

find ~/.cache/ -type f -atime +90 -delete

I also delete the older logs if no issues.

find ~/.cache/ -type f -atime +90 -delete

houseclean journalctl over 10 days

journalctl --vacuum-time=10d

Then if not typical cache we can search. cd / or cd /home

sudo du -hc --max-depth=1

Or and then for largest folder change from / to that folder - /var as an example and keep drilling down:

sudo du -hx --max-depth=1 / 2> /dev/null
sudo du -hx --max-depth=1 /var 2> /dev/null

I once forgot to mount my backup and it put the entire thing into /. I just barely had room, so system did not crash but root was almost full.

You also can check for large folders & files:

sudo du -h --max-depth=1 / | grep '[0-9]G\>'   # folders larger than 1GB
sudo find / -name '*' -size +1G    # files larger than 1GB

or install ncdu and drill down from / (q to quit):

sudo ncdu /
