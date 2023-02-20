Mailman 3 Ansible Role
======================

`galaxyproject.mailman3` is an Ansible role to install the [Mailman 3][mailman3] suite. This role installs all
components of the suite: Mailman 3 Core, and the Django-based web interfaces, Postorius and Hyperkitty.

Mailman 3 is a complicated service with many parts. It is a good idea to familiarize yourself with them before
proceeding. See the [architecture documentation][mailman3_arch] for details.

[mailman3]: https://docs.mailman3.org/
[mailman3_arch]: https://docs.mailman3.org/en/latest/architecture.html

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

Variables are described in detail in [`defaults/main.yml`](defaults/main.yml).

Dependencies
------------

There are no strict depdendencies, but production Mailman 3 services typically need Postfix and PostgreSQL. You may find
the following roles useful:

- [galaxyproject.postgresql](https://galaxy.ansible.com/galaxyproject/postgresql)
- [galaxyproject.postgresql_objects](https://galaxy.ansible.com/galaxyproject/postgresql_objects)
- [galaxyproject.postfix](https://galaxy.ansible.com/galaxyproject/postfix)
- [galaxyproject.opendkim](https://galaxy.ansible.com/galaxyproject/opendkim)
- [galaxyproject.nginx](https://galaxy.ansible.com/galaxyproject/nginx)

Example Playbook
----------------

A relatively simple, single-site setup using PostgreSQL as the database backend:

```yaml
- name: Install Mailman 3
  hosts: all
  vars:
    mailman3_django_superusers:
      - name: admin
        pass: admin
        email: admin@example.org
    mailman3_core_api_admin_user: adminuser
    mailman3_core_api_admin_pass: adminpass
    mailman3_archiver_key: archiverkey
    mailman3_config:
      mailman:
        site_owner: listmaster@example.org
      database:
        class: mailman.database.postgresql.PostgreSQLDatabase
        url: postgres:///mailman3_core?host=/var/run/postgresql
    mailman3_django_config:
      secret_key: supersecret
      hyperkitty_attachment_folder: "{{ mailman3_web_var_dir }}/attachments"
      databases:
        default:
          ENGINE: django.db.backends.postgresql_psycopg2
          NAME: mailman3_web
          HOST: /var/run/postgresql
    mailman3_extra_packages:
      - psycopg2-binary
```

A more complex setup with multiple list domains, Xapian haystack engine, distribution of Postfix lmtp maps to MX
servers, and DKIM:

```yaml
- name: Install Mailman 3
  hosts: all
  vars:
    mailman3_domains:
      - lists.example.org
      - lists.example.com
    mailman3_django_superusers:
      - name: admin
        pass: admin
        email: admin@example.org
    mailman3_core_api_admin_user: adminuser
    mailman3_core_api_admin_pass: adminpass
    mailman3_archiver_key: archiverkey

    mailman3_config:
      mailman:
        site_owner: listmaster@example.org
      mta:
        # bypass the content filter (amavisd-new) for Mailman messages since they were scanned on the way in
        smtp_port: 10025
      database:
        class: mailman.database.postgresql.PostgreSQLDatabase
        url: postgres:///mailman3_core?host=/var/run/postgresql
      arc:
        enabled: 'yes'
        privkey: "/etc/dkimkeys/mail.private"
        selector: mail
        domain: lists.example.org
        dmarc: 'yes'
        dkim: 'yes'
        authserv_id: lists.example.org
        trusted_authserv_ids: lists.example.org, lists.example.com, example.org

    mailman3_django_config:
      secret_key: supersecret
      use_x_forwarded_host: true
      hyperkitty_attachment_folder: "{{ mailman3_web_var_dir }}/attachments"
      databases:
        default:
          ENGINE: django.db.backends.postgresql_psycopg2
          NAME: mailman3_web
          HOST: /var/run/postgresql
      haystack_engine: xapian_backend.XapianEngine

    mailman3_extra_packages:
      - psycopg2-binary
      - xapian-haystack

    mailman3_distribute_maps:
      - host: all
        mailman3_distribute_maps_dir: "{{ mailman3_distribute_maps_dir }}"
        mailman3_postmap_command: /usr/sbin/postmap
      - host: mx1.example.org
      - host: mx2.example.org
      - host: mx3.example.org
```

License
-------

MIT

Author Information
------------------

The [Galaxy Community](https://galaxyproject.org/) and [contributors](https://github.com/galaxyproject/ansible-mailman3/graphs/contributors)
