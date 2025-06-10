# The publish tool is now distributed as a container image.  Simply
# pull the upstream image rather than cloning the repository at build
# time.  This avoids host dependencies and keeps secrets out of the
# Docker build context.

FROM ghcr.io/jpl-labcas/publish:latest

##
## No additional commands are required here.  The upstream image
## provides the ``publish`` entrypoint directly.  Any environment
## variables defined at run time will be passed through.
##

