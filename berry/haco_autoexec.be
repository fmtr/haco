def autoexec(metadata)

    import haco
    global.haco=haco

    haco.daemon=haco.Daemon()

    #haco.daemon.registry_daemon.remove_all()

end

var mod = module("haco_autoexec")
mod.autoexec=autoexec
return mod