This role can be included like any other role to install New Relic. It will automatically include the infra agent as a dependency

### Example
<p>

This role provides a few options that can customize the New Relic experience. A common configuration can be seen below:
```
---
- name: single host example
  hosts: localhost
  roles:
  - role: newrelic.infra.integration_mssql
    vars:
      nr_mssql_hostname: localhost
      nr_mssql_username: user
      nr_mssql_password: pass!
      nr_mssql_instance: INST01


- name: multihost example
  hosts: localhost
  roles:
  - role: newrelic.infra.integration_mssql
    vars:
      nr_mssql_hostname: localhost
      nr_mssql_username: user
      nr_mssql_password: pass!
      nr_mssql_instance: INST01
  - role: newrelic.infra.integration_mssql
    vars:
      nr_mssql_hostname: localhost
      nr_mssql_username: user1
      nr_mssql_password: pass!2
      nr_mssql_instance: INST02
```

</p>
