#!/bin/bash
set -e
echo "Running LDAP entrypoint script..."
if [ -f /tmp/ldap/init_ldap.sh ]; then
  chmod +x /tmp/ldap/init_ldap.sh
  echo "init_ldap.sh permissions set."
else
  echo "WARNING: /tmp/ldap/init_ldap.sh not found."
fi

set -e

# Start the LDAP server in the background
/opt/bitnami/scripts/openldap/run.sh &

# Wait for the LDAP server to be ready
until ldapsearch -x -H ldap://localhost -b "$LDAP_ROOT" -s base "(objectclass=*)" > /dev/null 2>&1; do
  echo "Waiting for LDAP server..."
  sleep 5
done

echo "LDAP server is up. Running initialization."

# Run the initialization script
/tmp/ldap/init_ldap.sh

# Keep the container running
tail -f /dev/null
