Role Name
=========

Install Mailman version 3, including either/all of Core, Postorius, Hyperkitty.

Mailman 3 is not trivial to set up.

Requirements
------------

The role does not include configuration of the MTA (exim, postfix, etc) which must be done
to get email in and out of Mailman Core. Mailman 3 (normally) uses LMTP to send/receive
mail, and canned condfigurations are available in many places.


Role Variables
--------------

Refer to default/main.yml for the role variables, which are somewhat documented there.

Some suggestions:

 - Unless you are using a multi-server postfix setup, you don't need to consider map directories.

 - To start with, you may wish to set mailman3\_uwsgi\_static true, so the python webserver
   provides these files, and consider configuring nginx, etc, to do that later

 - The main configuration is done by merging the default config dictionary with a custom
   (playbook-provided) one -- and some default items can be set individually as well, so there
   are two ways to define some items. In your playbook, most config can be set in "mailman3\_config":
   or "mailman3\_django":, which will be merged to make "\_\_mailman3\_config\_merged". In
   config.yml some debug actions are commented out, and enabling them may be helpful to understand
   what you have set.

 - You definitely need to change "mailman3\_core\_api\_admin\_pass" and "mailman3\_archiver\_key"!


Dependencies
------------

This role works well with rivimey.exim to configure the Exim MTA.

Example Playbook
----------------

These variables tell the role to install all 3 main components of MM3 on
the current host, which is addressed externally as mailman.example.org.


```
# These control which components of mailman are configured on this host. 
mailman3_run_m3core: yes
mailman3_run_m3client: yes
mailman3_run_m3core_host: mailman.example.org
# The role has had no testing with postorius host != hyperkitty host
mailman3_run_postorius: yes
mailman3_run_postorius_host: mailman.example.org
mailman3_run_hyperkitty: yes
mailman3_run_hyperkitty_host: mailman.example.org

# Postfix multi-server only
mailman3_distribute_maps: no

# Domains that lists can belong to, e.g. mylist@example.net:
mailman3_domains: [ 'example.net' ]

# File locations:
mailman3_install_dir: /opt/mailman3
mailman3_etc_dir: "{{ mailman3_install_dir }}/etc"
mailman3_var_dir: "{{ mailman3_install_dir }}/var/core"
mailman3_log_dir: "{{ mailman3_install_dir }}/var/core/log"
mailman3_django_var_dir: "{{ mailman3_install_dir }}/var/web"
mailman3_django_project_dir: "{{ mailman3_install_dir }}/var/web/project"
mailman3_django_static_dir: "{{ mailman3_install_dir }}/var/web/static"
mailman3_django_log_dir: "{{ mailman3_install_dir }}/var/web/log"
mailman3_django_settings_file: "{{ mailman3_install_dir }}/etc/django-settings.py"

# Basic setup:
mailman3_web_user: "www-data"
mailman3_web_group: "www-data"
mailman3_http_socket: "{{ mailman3_run_postorius_host }}:8880"
mailman3_archiver_key: "my-really-secret-key"
mailman3_core_api_hostname: "{{ mailman3_run_postorius_host }}"
mailman3_core_api_port: 8870
mailman3_core_api_admin_user: restadmin
mailman3_core_api_admin_pass: "the password to beat them all"
mailman3_admin_email_domain: ivimey.org
mailman3_uwsgi_static: yes

# Example config for exim4.
mailman3_config:
  mta:
    incoming: mailman.mta.exim4.LMTP
    outgoing: mailman.mta.deliver.deliver
    lmtp_host: mail.example.org
    lmtp_port: 8024
    smtp_host: mail.example.org
    smtp_port: 25
    configuration: python:mailman.config.exim4

mailman3_django_config:
  install_admin_app: yes
  debug: yes
  default_http_protocol: "http"
  secret_key: "you.will.never.guess.me"
  allowed_hosts:
    - "{{ mailman3_run_postorius_host }}"

```

License
-------

BSD

Author Information
------------------

Created by Nate Coraor @natefoo
dditional work by Ruth Ivimey-Cook @rivimey
