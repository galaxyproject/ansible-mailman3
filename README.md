Ansible Mailman3
================

Installs Mailman version 3, including either/all of Core, Postorius, or
Hyperkitty.

**Mailman 3 is not trivial to set up. Do not depend on a distro package
maintainer to do it for you**.

Mailman enables mailing lists to be managed on a mail server, can cope
with multiple virtual domains (e.g  both example.com and example.net),
deals with munging emails to account for DMARC and adding header and
footer parts, and takes care of list membership issues. However it
does require a properly set up Mail Transfer Agent (MTA) such as exim,
qmail, postfix or similar to both accept and deliver email.

This role is capable of working with several MTAs, but has been developed
alongside exim4 and as such may have glitches with other options.


Requirements
------------

The role does not include configuration of the MTA (exim, postfix, etc)
which must be done to get email in and out of Mailman Core. Mailman 3
(normally) uses LMTP to send/receive mail, and canned condfigurations are
available in many places.

The author's configuration uses Exim4 and MariaDB, with some help from
nginx purely as reverse proxy. The following roles may be of interest:

- [rivimey.ansible-mailman3](https://github.com/rivimey/ansible-mailman3)
- [rivimey.ansible\_dovecot](https://galaxy.ansible.com/rivimey/ansible_dovecot)
- [rivimey.ansible\_exim4](https://galaxy.ansible.com/rivimey/ansible_exim4)
- [galaxyproject.postgresql](https://galaxy.ansible.com/galaxyproject/postgresql)
- [galaxyproject.postgresql_objects](https://galaxy.ansible.com/galaxyproject/postgresql_objects)
- [galaxyproject.postfix](https://galaxy.ansible.com/galaxyproject/postfix)
- [galaxyproject.opendkim](https://galaxy.ansible.com/galaxyproject/opendkim)
- [galaxyproject.nginx](https://galaxy.ansible.com/galaxyproject/nginx)

It should be remembered that the MTA (Exim, postfix, etc) and mailman-core
must both know which mailing lists are configured. In Exim's case, this can
be done by exim checking which directories exist in the mailman install;
other MTAs have other ways to do this.


Role Variables
--------------

Refer to `default/main.yml` for the role variables, which are somewhat
documented there.

There are two 'halves' of mailman3: the Core, which does the actual work
of accepting email and running lists, and the Django web front end, which
enables admins and users to see some settings, add and remove members, etc,
using a web front end. The Django side interacts with the Core using a REST
API, and if this link breaks the Web side wont work, but the Core will.

Given this split, the role variables are also split in the same way, and
this ansible role enables you to place core and django on different hosts.
Be aware, though, that a one-host solution will be simpler to start with.

Most configuration is done by merging the default config dictionary with a
custom (playbook-provided) dict. Some default items can be set individually
as well, so there are two ways to define some items.

In your playbook, most config can be set in your playbook's "mailman3\_config"
or "mailman3\_django" keys, which will be merged with the default keys to
make "\_\_mailman3\_config\_merged" and "\_\_mailman3\_django\_config\_merged",
respectively.

In the config.yml some debug actions are commented out, and temporarily
enabling them may be helpful to understand what you have set.

Some suggestions:

 - By default mailman creates an sqlite3 db to store archived mail. This
   is fine for experimenting but it is later problematic to migrate to
   a larger db (mysql, mariadb, postgres). Do not use sqlite for
   non-trivial use-cases.

 - Unless you are using a multi-server postfix setup, you don't need to
   consider map directories.

 - To start with, you may wish to set mailman3\_uwsgi\_static true, so the
   python webserver provides these files, and consider configuring nginx,
   etc, to do that later


 - You definitely need to change "mailman3\_core\_api\_admin\_pass" and
   "mailman3\_archiver\_key"!


Dependencies
------------

This role works well with the rivimey/exim role to configure the Exim MTA,
but does not require it.

It is however necessary for an MTA to be available, to both deliver mail to
mailman3 (over LMTP) and to accept mail for distribution from it (over SMTP).


Example Playbook
----------------

These variables tell the role to install all 3 main components of MM3 on
the current host, which is addressed externally as mailman.example.org.

**Note: the notation `# key: [vault]` means the variable should be defined in
your ansible vault, and so it is commented out in this yaml set**.

```
# These control which components of mailman are configured on which host.

# Define which parts of mailman run on this host, and which hosts are involved.
mailman3_run_m3core: yes
mailman3_run_m3client: yes
mailman3_run_m3core_host: mailman-core.example.org
mailman3_run_postorius: no
mailman3_run_postorius_host: lists.example.org
mailman3_run_hyperkitty: no
mailman3_run_hyperkitty_host: lists.example.org
mailman3_distribute_maps: no

# Database selection, passwords
mailman3_core_db_host: mailman-core.ivimey.org
# Select the DB backend. 'mysql' includes 'mariadb'
mailman3_core_db_type: mysql    # sqlite3 | postgres | mysql
# mailman_db_password: [vault]
# mailman_webdb_password: [vault]

# Postfix multi-server only
mailman3_distribute_maps: no

# Domains that lists can belong to, e.g.
#   My Mailing List <my-list@dom.ain.example.uk>
# would need:
mailman3_domains: [ 'dom.ain.example.uk' ]

# File locations:
# Using /opt here avoids unfortunate interaction with other installs.
mailman3_install_dir: /opt/mailman3

# mailman3_archiver_key: [vault]
mailman3_etc_dir: "{{ mailman3_install_dir }}/etc"
mailman3_var_dir: "{{ mailman3_install_dir }}/var/core"
mailman3_log_dir: "{{ mailman3_install_dir }}/var/core/log"
mailman3_django_var_dir: "{{ mailman3_install_dir }}/var/web"
mailman3_django_project_dir: "{{ mailman3_install_dir }}/var/web/project"
mailman3_django_packages_dir: "{{ mailman3_install_dir }}/lib/{{ mailman3_python_version }}/site-packages"
mailman3_django_static_dir: "{{ mailman3_install_dir }}/var/web/static"
mailman3_django_log_dir: "{{ mailman3_install_dir }}/var/web/log"
mailman3_django_settings_file: "{{ mailman3_install_dir }}/etc/django-settings.py"

# As part of a pathname:
mailman3_python_version: python3.10

# Basic setup:
mailman3_web_user: "www-data"
mailman3_web_group: "www-data"
# Listen socket & "self_linK" hostname/port
mailman3_http_socket: "{{ mailman3_run_postorius_host }}:8880"
mailman3_postorius_listen_address: "0.0.0.0"
mailman3_core_api_hostname: "{{ mailman3_run_m3core_host }}"
mailman3_core_api_port: 8870
mailman3_core_api_admin_user: restadmin
# mailman3_core_api_admin_pass: [vault]
# mailman3_django_secret_key: [vault]
mailman3_admin_email_domain: example.org
mailman3_uwsgi_static: yes
mailman3_virtualenv_command: virtualenv


# Example config for exim4.
mailman3_config:
  mailman:
    site_owner: root@example.org
    noreply_address: noreply
    html_to_plain_text_command: /usr/bin/lynx -dump $filename
  mta:
    incoming: mailman.mta.exim4.LMTP
    outgoing: mailman.mta.deliver.deliver
    lmtp_host: post.example.org
    lmtp_port: 8024
    smtp_host: post.example.org
    smtp_port: 25
    configuration: python:mailman.config.exim4


mailman3_django_config:
  webservice:
    protocol: https
    hostname: "{{ mailman3_run_postorius_host }}"
    port: 8880
    listen: 0.0.0.0
  # The Django database.
  databases:
    default:
      ENGINE: django.db.backends.mysql
      NAME: mailmanweb
      USER: mailmanweb
      PASSWORD: "{{ mailman_db_password }}"
      HOST: "localhost"

  install_admin_app: yes
  debug: no
  memcache_enabled: yes
  #  [__mailman3_django_secret_key in vault]
  secret_key: "{{ __mailman3_django_secret_key }}"
  allowed_hosts:
    - "{{ mailman3_run_m3core_host }}"
    - "{{ mailman3_run_postorius_host }}"
    - "{{ mailman3_core_api_hostname }}"
```

License
-------

BSD

Author Information
------------------

Created by Nate Coraor @natefoo
Developed and Maintained by Ruth Ivimey-Cook @rivimey

