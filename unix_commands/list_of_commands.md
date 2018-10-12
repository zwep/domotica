Here we show a list of commands I have used or had to use frequently.


## Connect

Most secure way...
```sh
ssh USERNAME@ADRES 
```

## File management

Useful tools
* Graphical Disk Map

To see the current disk usage, in readable form, for a limited depth, use
```bash
du -h --max-depth=1 /path/to/folder
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


## Scheduling

Use cron for this, you can edit the jobs via
```bash
crontab -e
```

