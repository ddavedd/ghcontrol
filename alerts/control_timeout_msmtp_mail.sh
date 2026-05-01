msmtp david.j.smits@gmail.com << EOF
TO: David <david.j.smits@gmail.com>,
FROM: Automated Warning System <halfacreplainfield@gmail.com>
SUBJECT: $(id -un) reports control temperature timeout

$(id -un) temperature has not been updated, possible crash of temperature_read.py
EOF

