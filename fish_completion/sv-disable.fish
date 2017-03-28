complete -c sv-disable -a "(/bin/ls /var/service/)" -f -d 'Service'
complete -c sv-disable -l help -s h -d 'Show the help and exit'
complete -c sv-disable -l sv-dir -s A -d 'Path to directory containing your service\'s run script.  Default: /etc/sv'
complete -c sv-disable -l runsvdir -s B -d 'Path to your runsvdir. Default: /var/service'
