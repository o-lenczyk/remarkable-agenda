## Goal
Goal of this project is to display upcoming tasks / meetings using Remarkable screen saver.  
Necessary steps:
- download all planned tasks from Google Calendar
- transform it to an image
- set as Remarkable screen saver

## Automatiom
- Github Actions will fetch the agenda and create an image
- Systemd timer will fetch the screen saver, next time when device is turned on

## Setting up Systemd timer
- login via ssh to Remarkable
- edit `/etc/systemd/system/agenda.service`
  ```
  #  SPDX-License-Identifier: LGPL-2.1+

  [Unit]
  Description=Remarkable Agenda
  DefaultDependencies=no
  Conflicts=shutdown.target
  Before=basic.target shutdown.target

  [Service]
  Type=oneshot
  ExecStart=date
  StandardOutput=append:/home/root/a
  SuccessExitStatus=DATAERR
  IOSchedulingClass=idle
  ```
- edit `/etc/systemd/system/agenda.timer`
  ```
  #  SPDX-License-Identifier: LGPL-2.1+

  [Unit]
  Description=Remarkable Agenda Timer
  Documentation=someday

  [Timer]
  OnStartupSec=5min
  OnCalendar=*:0/1
  OnUnitActiveSec=1d

  [Install]
  WantedBy=timers.target
  ```
- enable timer: `systemctl enable agenda.timer`
- start timer: `systemctl start agenda.timer`
- list timers: `systemctl list-timers`