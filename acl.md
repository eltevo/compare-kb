# Managing ACLs

Reset ACL permissions, keep posix permissions only:

    # setfacl -Rb .

Grant full access to the entire tree for debugging:

    # setfacl -Rm u:dobos:rwx /srv/kooplex/compare/
