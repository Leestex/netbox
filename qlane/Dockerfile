# qlane test target: runs THIS repository's NetBox source (the pull request's code) on the
# official image's runtime (Python venv, entrypoint, container configuration).
#
# The base image's own app directory is replaced wholesale by the repository's `netbox/`, so a
# file the pull request deletes is gone here too. Kept from the base: the four container files
# the image adds (configuration.py, granian.py, ldap_config.py, local/release.yaml) and the built
# documentation. Python dependencies are re-synced from the repository's requirements.txt.
FROM docker.io/netboxcommunity/netbox:v4.7.2-5.1.1

RUN mkdir -p /opt/qlane-keep/netbox /opt/qlane-keep/local \
 && cp -a /opt/netbox/netbox/netbox/configuration.py /opt/netbox/netbox/netbox/granian.py \
          /opt/netbox/netbox/netbox/ldap_config.py /opt/qlane-keep/netbox/ \
 && cp -a /opt/netbox/netbox/local/release.yaml /opt/qlane-keep/local/ \
 && mv /opt/netbox/netbox/project-static/docs /opt/qlane-keep/docs \
 && rm -rf /opt/netbox/netbox

COPY requirements.txt /opt/netbox/requirements.txt
RUN uv pip install --python /opt/netbox/venv/bin/python --no-cache -r /opt/netbox/requirements.txt

COPY netbox/ /opt/netbox/netbox/
RUN cp -a /opt/qlane-keep/netbox/. /opt/netbox/netbox/netbox/ \
 && mkdir -p /opt/netbox/netbox/local && cp -a /opt/qlane-keep/local/. /opt/netbox/netbox/local/ \
 && mv /opt/qlane-keep/docs /opt/netbox/netbox/project-static/docs \
 && rm -rf /opt/qlane-keep \
 && SECRET_KEY="qlane-build-time-placeholder-not-used-at-runtime-0123456789abcdef" \
    /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py collectstatic --no-input --verbosity 0
