msmtp david.j.smits@gmail.com << EOF
TO: David <david.j.smits@gmail.com>,
FROM: Automated Warning System <halfacreplainfield@gmail.com>
SUBJECT: $(id -un) reports high temperature

$(id -un) temperature high, check to ensure controls are working
EOF

