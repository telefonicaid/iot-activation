export
eclipse_home=C:\ProgramData\Telit\IoT_AppZone_IDE\eclipse
SDK_VERSION=4.2.1
FW_VERSION=30_00_xx7-B004
LOGONSERVER= 
PLUGIN_VERSION=0.7.4.302011
APPZONE_DIR=${eclipse_home}\\plugins\com.telit.appzonec.plugin.me910_ml865_${FW_VERSION}_${PLUGIN_VERSION}
APPZONE_LIB=$(APPZONE_DIR)\lib
TOOLCHAIN_PATH=${eclipse_home}\\plugins\com.telit.appzonec.toolchain.plugin.gccARMv6_493_4.9.3
APPZONE_INC=$(APPZONE_DIR)\m2m_inc
APPZONE_MAKEFILE=$(APPZONE_DIR)\makefiles
APPZONE_BIN=${eclipse_home}\\plugins\com.appzonec.plugin.prebuilt_$(SDK_VERSION)\prebuilt\bin
APPZONE_MAKEFILE_COMMON=${eclipse_home}\\plugins\com.appzonec.plugin_$(SDK_VERSION)\makefiles
TOOLCHAIN_BIN=${eclipse_home}\\plugins\com.telit.appzonec.toolchain.plugin.gccARMv6_493_4.9.3\arm_gcc493/bin/
OUTOBJDIR=obj
AZ_BASE_MAKEFILE=az_makefile.mk
LIB_PATH=-L "${eclipse_home}\\plugins\com.telit.appzonec.toolchain.plugin.gccARMv6_493_4.9.3\arm_gcc493/lib/gcc/arm-none-eabi/4.9.3" -L "${eclipse_home}\\plugins\com.telit.appzonec.toolchain.plugin.gccARMv6_493_4.9.3\arm_gcc493/arm-none-eabi/lib" 
AZ_STATIC_LIB=FALSE
