msmtp david.j.smits@gmail.com << EOF
TO: David <david.j.smits@gmail.com>,
FROM: Automated Warning System <halfacreplainfield@gmail.com>
SUBJECT: $(id -un) Test Mail

$(id -un) test msmtp email
EOF

