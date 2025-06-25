#!/bin/bash
set -e

echo "Sleeping 30 seconds..."
sleep 30

# ------------------------------------------------------------------
# Ensure the LabCAS backend trusts the LDAP server certificate.
# This grabs the server's cert from ldaps://ldap:1636 at runtime and
# imports it into the container's default Java trust-store (cacerts)
# under alias “ldap-cert” if it is not already present.  This avoids
# any mismatch between host-generated and image-generated certificates.
# ------------------------------------------------------------------
# Certificate steps may fail transiently (e.g., LDAP not yet up); do
# NOT let that abort the whole container. Temporarily disable 'set -e'.
set +e
LDAP_HOST=${LDAP_HOST:-ldap}
LDAP_PORT=${LDAP_PORT:-1636}

# Resolve the path to cacerts (works for any JDK layout)
CACERTS_PATH=$(keytool -list -keystore "$(dirname "$(readlink -f "$(which java)")")/../lib/security/cacerts" -storepass changeit >/dev/null 2>&1 && \
               echo "$(dirname "$(readlink -f "$(which java)")")/../lib/security/cacerts")
# Fallback to JAVA_HOME if the above failed
if [ -z "$CACERTS_PATH" ] && [ -n "$JAVA_HOME" ]; then
  CACERTS_PATH="$JAVA_HOME/lib/security/cacerts"
fi

if ! keytool -list -alias ldap-cert -keystore "$CACERTS_PATH" -storepass changeit >/dev/null 2>&1; then
  echo "Importing LDAP certificate into Java cacerts..."
  # Pull the cert from the running LDAP server
  echo | openssl s_client -connect "${LDAP_HOST}:${LDAP_PORT}" -showcerts 2>/dev/null \
       | sed -n '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/p' \
       > /tmp/ldap-cert.pem

  if [ -s /tmp/ldap-cert.pem ]; then
      keytool -importcert -noprompt -trustcacerts -alias ldap-cert \
              -file /tmp/ldap-cert.pem -keystore "$CACERTS_PATH" \
              -storepass changeit
      echo "LDAP certificate imported successfully."
  else
      echo "WARNING: could not retrieve LDAP certificate; LDAPS may fail."
  fi
else
  echo "LDAP certificate already trusted."
  fi
  # Re-enable strict error handling for the remainder of the script
  set -e

if [ -f "/tmp/labcas/start.sh" ]; then
  echo "Running start.sh..."
  /bin/bash /tmp/labcas/start.sh
else
  echo "start.sh not found."
fi

if [ -f "/tmp/labcas/init_solr.sh" ]; then
  echo "Running init_solr.sh..."
  /bin/bash /tmp/labcas/init_solr.sh
else
  echo "init_solr.sh not found."
fi

echo "Starting tail -f /dev/null to keep container alive."
exec tail -f /dev/null
