complete -c sv-enable -a "(/bin/ls /etc/sv/)" -f -d 'Service'
complete -c sv-enable -l help -s h -d 'Show the help and exit'
complete -c sv-enable -l sv-dir -s A -d 'Path to directory containing your service\'s run script.  Default: /etc/sv'
complete -c sv-enable -l runsvdir -s B -d 'Path to your runsvdir. Default: /var/service'
