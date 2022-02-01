##cli-verification

###Scripts
`min_frr_config.sh`: Runs a minimal setup of FRR on Docker
`make_command.py`: Configuration command creation from template
`generate_configs.py`: Generates expect scripts containing all possible combinations of commands

###Config files
`vtysh.conf`: vtysh configuration file
`bgpd.conf`: bgpd configuration file
`config_templates`: consisting of command templates retrieved by running the `list` command in vtysh - taken in as input by generate_configs.py


