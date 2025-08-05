#!/bin/bash
set -e

echo "Sleeping 30 seconds..."
sleep 30

# -------------------------------------------------------------------
# Ensure the LabCAS backend can always trust the LDAP server certificate
# -------------------------------------------------------------------
# Grab the current certificate from the ldap service and import it into
# the JVM truststore inside this container every time it starts.  This
# makes the trust persistent across container rebuilds without baking the
# cert into the image and avoids handshake failures like:
#   javax.naming.CommunicationException: simple bind failed
#
# NOTE: Any import errors (duplicate alias, etc.) are ignored.
echo "Importing LDAP certificate into Java cacerts truststore..."
openssl s_client -connect ldap:1636 -servername ldap -showcerts </dev/null 2>/dev/null | \
  awk '/BEGIN CERTIFICATE/{flag=1}/END CERTIFICATE/{print;flag=0}flag' > /tmp/ldap-cert.pem || true
keytool -importcert -noprompt -alias labcas-ldap-cert \
  -file /tmp/ldap-cert.pem \
  -keystore "$JAVA_HOME/jre/lib/security/cacerts" \
  -storepass changeit 2>/dev/null || true
rm -f /tmp/ldap-cert.pem

# -------------------------------------------------------------------
# Disable endpoint (hostname) verification for LDAP connections so the
# self-signed certificate with CN=localhost is accepted even though the
# service DNS name is simply “ldap”.
# Ensure this flag is propagated to every JVM started by the LabCAS
# startup scripts.
export JAVA_OPTS="-Dcom.sun.jndi.ldap.object.disableEndpointIdentification=true ${JAVA_OPTS}"
export CATALINA_OPTS="$JAVA_OPTS"
echo "DEBUG: CATALINA_OPTS set to $CATALINA_OPTS"

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