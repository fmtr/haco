var VERSION='0.0.23'

var mod = module("haco_version")
mod.VERSION=VERSION
mod.METADATA=(global.TAPP_METADATA!=nil?global.TAPP_METADATA:{}).find('haco',{})
mod.CHANNEL_ID=mod.METADATA.find('channel_id')

return mod