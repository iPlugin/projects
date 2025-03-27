include $(TOPDIR)/rules.mk

PKG_NAME:=netrouter
PKG_VERSION:=1.0
PKG_RELEASE:=0

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/uclibc++.mk
include $(INCLUDE_DIR)/package.mk

define Package/netrouter
	SECTION:=utils
	CATEGORY:=Utilities
	TITLE:=Netrouter project using raw sockets
	DEPENDS:=+libstdcpp
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

TARGET_CFLAGS += \
	-I$(STAGING_DIR)/usr/include \
	-D_GNU_SOURCE \
	-ggdb3

MAKE_FLAGS += \
	CFLAGS="$(TARGET_CFLAGS)" \
	LDFLAGS="$(TARGET_LDFLAGS)"

define Build/Compile
	$(call Build/Compile/Default, \
		CCOPTS="$(TARGET_CFLAGS)" \
		INCLUDE="$(EXTRA_CFLAGS)" \
		LDFLAGS="$(EXTRA_LDFLAGS)" \
	)
endef

define Package/netrouter/install
	$(INSTALL_DIR) $(1)/bin
	$(CP) $(PKG_BUILD_DIR)/$(PKG_NAME) $(1)/bin/
endef

$(eval $(call BuildPackage,netrouter))