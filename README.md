## Goal
Goal of this project is to display upcoming tasks / meetings from Google Calendar using Remarkable screen saver.  
Necessary steps:
- download all planned tasks from Google Calendar
- transform it to an image
- set as Remarkable screen saver

## Automation
- Github Actions will fetch the agenda and create an image
- Systemd timer will fetch the screen saver, next time when device is turned on
- `xochitl` will be restarted (couple of seconds) to reload suspended screen image

## cron vs Systemd timer
Cron is not installed by default on Remarable. It is possible to install it via [tolec](https://toltec-dev.org/), but it still does not make much sense, because cron is suspended, when Remarkable is in sleep mode. Because of that, is very easy to miss cron trigger. Advantage of Systemd timer is persistence - it will be triggered right after device is started / resumed.

## Setting up Systemd timer
- login via ssh to Remarkable
- edit `/etc/systemd/system/agenda.service`
  ```
  [Unit]
  Description=Remarkable Agenda
  DefaultDependencies=no
  Conflicts=shutdown.target
  Before=basic.target shutdown.target

  [Service]
  Type=oneshot
  ExecStartPre=wget --no-check-certificate "https://github.com/o-lenczyk/remarkable-agenda/raw/main/agenda.png" -O /usr/share/remarkable/suspended.png
  ExecStart=systemctl restart xochitl
  StandardOutput=/home/root/agenda.log
  SuccessExitStatus=DATAERR
  IOSchedulingClass=idle
  Restart=on-failure
  RestartSec=10
  ```
- edit `/etc/systemd/system/agenda.timer`
  ```
  [Unit]
  Description=Remarkable Agenda Timer
  Documentation=someday
  After=network-online.target

  [Timer]
  OnStartupSec=5min
  OnCalendar=07:00:00
  OnUnitActiveSec=1d
  Persistent=true

  [Install]
  WantedBy=timers.target
  ```
- enable timer: `systemctl enable agenda.timer`
- you can trigger timer manually: `systemctl start agenda.timer`
- list timers: `systemctl list-timers`
- output should be similar to:
  ```
  NEXT                         LEFT     LAST                         PASSED       UNIT                         ACTIVATES
  Tue 2022-01-18 07:00:00 UTC  7h left  Mon 2022-01-17 23:09:35 UTC  1min 41s ago agenda.timer                 agenda.service
  Tue 2022-01-18 20:40:55 UTC  21h left Mon 2022-01-17 09:54:17 UTC  13h ago      systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
  ```

## Setting up the repository
Set up those repository secrets:
- `CLIENT_ID`
- `CLIENT_SECRET`
- `DEFAULT_CALENDAR`
- `GCALCLI_OAUTH`

## How to get those secrets?
Folow those [instructions](https://github.com/insanum/gcalcli#howto) and configure [gcalcli](https://github.com/insanum/gcalcli) locally first.