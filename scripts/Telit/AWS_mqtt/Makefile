# If you would like to customize some of the build options for your AppZone
# C application, please create a file called Makefile.in in the same folder as
# the project and define one of the variables below:
# - to fully rebuild a project each time:
#   CLEAN_BEFORE_BUILD = clean
# - to add new include paths:
#   CPPFLAGS += -I my_hdr
# - to compile source files from another location into your project:
#   OBJS += $(patsubst %.c,%.o,$(wildcard my_src/*.c)) 
# - to change the name of the binary (it will still have .bin extension):
#   TELITBIN = myapp.0.1
#

CPPFLAGS=
LDFLAGS=
CFLAGS=
OBJS=

include prod_tool.in
-include Makefile.in
include export.mk




space :=
space += 
makefilePath := $(APPZONE_MAKEFILE_COMMON)/$(AZ_BASE_MAKEFILE)
makefilePath := $(subst $(space),\$(space),$(makefilePath))
include $(makefilePath)
