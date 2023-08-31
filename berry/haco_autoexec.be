def autoexec(metadata)

    import haco
    global.haco=haco

    haco.daemon=haco.Daemon()

end

var mod = module("haco_autoexec")
mod.autoexec=autoexec
return mod