Here we show a list of commands I have used or had to use frequently.


## Connections

A way to connect to a remote address
```sh
ssh USERNAME@ADRES 
```

Easy way to copy your ssh key to a new server
```bash
cp $HOME/.ssh/id_rsa.pub user@address:~/.ssh/authorized_keys
```

A way to send stuff to a remote address
```bash
scp /path/to/file USERNAME@location:/path/to/dest
```

What wifi is there?
```bash
nmcli dev wifi
```

What are my ports doing?
```bash
netstat -l
```

Can I connect with this port? (some ip adress, and some port)
```bash
telnet 192.168.178.1 8888
```

Having Citrix SSL error 61? (This is oddly specific btw)
```bash
sudo ln -s /usr/share/ca-certificates/mozilla/* /opt/Citrix/ICAClient/keystore/cacerts
```

(Port forwarding) Want to transfer data from remote port to local? Check this out
```bash
ssh -L 16006:127.0.0.1:6006 user@my_server_ip
```

Check if mysql is running...
```bash
systemctl status mysql.service
```
## File management

Useful tools
* Graphical Disk Map

To see the current disk usage, in readable form, for a limited depth, use
```bash
du -h --max-depth=1 /path/to/folder
```

Move certain files (recursively) to a new location, and thus maintaining the folder structure.

``` bash
 rsync -avm --include='*.list' -f 'hide,! */' . /home/charmmaria/Documents/Promoveren/data/mri_datalist/misc_data_list_2
```


## Navigation

Of course... the most easiest commands
```bash
ls
ll 
cd
cd ..

```

## External file management

Useful tools:
* Gparted
* Disks (native)

To see which partitions are found, check
```bash
lsblk
```
To mount something do
```bash
mount /dev/sdX /media/FOLDERNAME
```

To make sure that you device is mounted to the same folder each time, label your device like so
```bash
tune2fs -L LABELNAME /dev/sdX
```

To make sure that the current user can write to the device, make sure that you are the owner
```bash
chown USERNAME: /media/USERNAME/LABELNAME
chmod u+w /media/USERNAME/LABELNAME
```

To erase all the data on a drive, use
```bash
shred -vzn 0 /dev/sdX
```

## System behaviour

Want to rage-quit?
```bash
shutdown -h now
```

Want to see how nvidia is doing?
```bash
watch -n 1 nvidia-smi
```

Want to see why starting up takes so long?
```bash
systemctl list-units --type services
```

Want to see why everything is so slow?
```bash
top
```

or 

```bash
ps
```

Want to see why startup takes so long?
```bash
systemd-analyze blame
```

## Package management

Shows list of all libraries installed
```bash
dpkg -l
```



## Scheduling

Use cron for this, you can edit the jobs via
```bash
crontab -e
```

## Database management

For MySQL, want to know which paramters are set?
```bash
show variables;
```

## Specific actions

If you want to move a set of documents, that satisfy a certain collective regex naming convention, towards a specific
 destination... We can execute
 
 ```bash
 ➜  find . -name "REGEXPATTERN" | xargs mv -t path/to/your/destination
```

## Running background tasks

Here we will explain often used commands to run tasks in the background

# screens

# tmux

To start a session
```bash
tmux new -s 'session name'
```

To attach a session
```bash
tmux attach -t `session name
```

To detach when in a session
```
Ctrl+B+D
```

To remove/kill all sessions
```bash
tmux list-sessions | grep -v attached | awk 'BEGIN{FS=":"}{print $1}' | xargs -n 1 tmux kill-session -t || echo No sessions to kill
```