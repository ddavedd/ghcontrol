msmtp david.j.smits@gmail.com << EOF
TO: David <david.j.smits@gmail.com>,
FROM: Automated Warning System <halfacreplainfield@gmail.com>
SUBJECT: $(id -un) reports no temperature file found

$(id -un) temperature file not found, control will not work
EOF

