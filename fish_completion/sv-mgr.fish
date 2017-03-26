complete -c sv-mgr -p /usr/bin/sv-mgr -a "(/bin/ls /var/service/)" -l disable -x
complete -c sv-mgr -p /usr/bin/sv-mgr -a "(/bin/ls /etc/sv/)" -l enable -x
complete -c sv-mgr -p /usr/bin/sv-mgr -a "(/bin/ls /var/service/)" -s d -x
complete -c sv-mgr -p /usr/bin/sv-mgr -a "(/bin/ls /etc/sv/)" -s e -x
complete -c sv-mgr -p /usr/bin/sv-mgr -f -l help -l list -l sv-dir -l runsvdir -s A -s B -s h -s l
