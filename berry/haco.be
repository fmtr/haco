import tools, string, json, mqtt

var mod = module("haco")

import haco_version

var IS_DEVELOPMENT=haco_version.CHANNEL_ID=='development'

var logger=tools.logging.Logger(
    'haco',
    IS_DEVELOPMENT?tools.logging.Logger.DEBUG_MORE:tools.logging.Logger.INFO,
    IS_DEVELOPMENT
)

tools.logger.logger=logger

var CALLBACK_MAP={}
var BRANCH='release'

mod.CONFIG_APPLIED=false

for callback_type: [tools.callbacks.Rule,tools.callbacks.Timer,tools.callbacks.Cron]

	CALLBACK_MAP[classname(callback_type)]=callback_type
end

class ConfigDownloader

    static var PART_DELAY_SECS=2
    var parts
    var registry
    var callback_complete
    var id_downloading

    def init(callback_complete)
                
        self.parts=[]
        self.registry=tools.callbacks.Registry()
        self.callback_complete=callback_complete

    end

    def handle_config_message(config_data)
        
        var num_parts = config_data["size"]
        var id = config_data["id"]


        if self.id_downloading && self.id_downloading==id
            logger.debug(string.format("Got duplicate new config (same as currently being downloaded) ID: %s. Will be ignored.",id))
            return
        end



        if self.id_downloading
            logger.error(string.format("Got new config ID: %s while existing download ID: %s incomplete.",id,self.id_downloading))
        end

        logger.info(string.format("Downloading new config. ID: %s. Parts: %s",id,num_parts))

        self.id_downloading=id

        logger.debug(['Cancelling any existing downloads...'])        
        self.registry.remove_all()

        self.parts = []
        for i:0..num_parts-1
            self.parts.push(nil)
        end        
        
        var rule
        for i:0..num_parts-1

            var topic = string.format('haco/%s/%s/config/%s',BRANCH,tasmota.hostname(),i)
            var delay_trigger = string.format('delay:%s',topic)
            
            def callback_function(value)                            

                var id_part=value['id']
                var data=value['data']

                if id_part!=id
                    logger.error(string.format('Part %s of %s ID did not match config ID (%s!=%s). Skipping...',i+1,num_parts,id_part,id))
                    return
                end                

                logger.debug(string.format("Received Part %s of %s ID: %s Data: %s bytes",i+1,num_parts,id,size(data)))
                self.parts[i] = data
                #self.registry.remove(topic)
                #self.registry.remove(delay_trigger)

                self.check_complete()

            end

            def delay_wrap()
                var rule_delay=tools.callbacks.MqttSubscription(topic,callback_function)
                self.registry.add(rule_delay)
            end
            
            rule=tools.callbacks.Timer((self.PART_DELAY_SECS*1000)*(i+1),delay_wrap,delay_trigger)

            self.registry.add(rule)



        end
    end

    def check_complete()

        var num_missing=self.num_missing()

        if num_missing
            logger.debug(string.format("Config is not yet complete. Awaiting %s of %s parts.",num_missing,size(self.parts)))
        else
            logger.debug(string.format("Config is complete."))
            var config_complete=self.collate()
            self.parts=[]
            self.registry.remove_all()
            self.id_downloading=nil
            self.callback_complete(config_complete)
        end

    end

    def collate()

        var config_str=self.parts.concat()        
        logger.debug_more(string.format('Collated raw config string. Size: %s bytes.',size(config_str)))

        var config=json.load(config_str)     
        logger.debug_more(string.format('Deserialized config string. Size: %s fields.',size(config)))

        return config

    end

    def num_missing()
        var count=0
        for message:self.parts
            if message==nil count+=1 end
        end
        return count

    end

    def close()
        self.registry.remove_all()
    end


end


class Daemon

    static var DELAY_APPLY=30
    static var DELAY_SUBSCRIBE=30

    var registry_daemon
    var registry_config
    var downloader
    var config_id
    var mqtt_data



    static var TOPIC_CONFIG=string.format('haco/%s/%s/config',BRANCH,tasmota.hostname())
    static var TOPIC_CONTROL=string.format('haco/%s/%s/control/+/+/tasmota/in',BRANCH,tasmota.hostname())
    static var TOPIC_ANNOUNCE=string.format('haco/%s/%s/announce',BRANCH,tasmota.hostname())

    def init()

        logger.info(string.format('Starting haco daemon (v%s) in %s seconds...',haco_version.VERSION, self.DELAY_SUBSCRIBE))

        self.registry_daemon=tools.callbacks.Registry()
        self.registry_config=tools.callbacks.Registry()
        self.mqtt_data={}
        self.downloader=ConfigDownloader(/configs->self.apply_configs(configs))

        var rule_subscribe_daemon=tools.callbacks.Timer(self.DELAY_SUBSCRIBE*1000,/->self.subscribe_daemon())
        self.registry_daemon.add(rule_subscribe_daemon)

    end

    def subscribe_daemon()

        var rule_announce=tools.callbacks.Rule('mqtt#connected',/->self.publish_announce())
        self.registry_daemon.add(rule_announce)

        var rule_config=tools.callbacks.MqttSubscription(
            self.TOPIC_CONFIG,
            /value->self.handle_config_message(value)
        )
        self.registry_daemon.add(rule_config)

        if mqtt.connected() self.publish_announce() end

        logger.info(string.format('The haco daemon has started. Hostname: %s, MAC: %s. Listening for configuration...', tasmota.hostname(), tools.network.get_mac()))

    end

    def handle_config_message(data)

        if data['id']==self.config_id && (!data["force_update"])
            logger.error(string.format('Received duplicate config ID: %s. Will be ignored.',self.config_id))
            return
        end

        self.downloader.handle_config_message(data)

    end

    def publish_announce()        
        var data=self.get_data_announce()        
        logger.debug(['Publishing announce data...'])
        return tools.mqtt.publish_json(self.TOPIC_ANNOUNCE,data,true)
    end

    def get_data_announce()

        return {
            'version': haco_version.VERSION,
            'hostname': tasmota.hostname(),
            'eth': tasmota.eth(),
            'wifi': tasmota.wifi(),
            'mac': tools.network.get_mac(),
            'timestamp': tasmota.rtc(),
            'config_id': self.config_id,
            'topic': tools.mqtt.get_topic(),
            'device_name': tools.platform.get_device_name(),
        }
    end

    def apply_configs(data)

        logger.debug(string.format('Clearing existing config ID %s...',self.config_id))
        self.registry_config.remove_all()

        var id=data['id']
        logger.info(string.format('Applying new config ID %s...',id))

        var rule
        for config_cb: data['callbacks']
            rule=self.apply_config_callback(config_cb)
            self.registry_config.add(rule)
        end

        var mqtt_data=data['mqtt']
        for topic: mqtt_data.keys()
            mqtt_data[topic]['function']=tools.compile.evaluate(mqtt_data[topic]['function'])
        end

        self.mqtt_data=mqtt_data

        var run_config_post=data['run_config_post']
        if run_config_post
            logger.info(['Running run_config_post',tools.compile.evaluate(run_config_post)()])
        end

        if self.config_id==nil
            var rule_control=tools.callbacks.MqttSubscription(
                self.TOPIC_CONTROL,
                /value,data->tasmota.set_timer(0,/->self.handle_control_message(value,data))
            )
            self.registry_daemon.add(rule_control)
        end
        
        self.config_id=id
        self.publish_announce()

        logger.info(string.format('New config ID %s applied successfully.',id))

    end

    def handle_control_message(value,data)

        var mqtt_data=self.mqtt_data[data['topic']]
        var topic=mqtt_data['topic']
        var function=mqtt_data['function']

        logger.debug_more(['mqtt<- ', data['topic'], value])

        return self.publish_output(function,value,data,topic)

    end

    def publish_output(function,value,data,topic)

        var output=function(value,data)

        if topic!=nil
            logger.debug_more(['mqtt-> ', data['registration'].id ,topic, output])
            tools.mqtt.publish_json(topic,output)
        end

    end


    def apply_config_callback(data)

        var callback_type=CALLBACK_MAP[data.find('type', classname(tools.callbacks.Rule))]
        var topic=data['topic']
        var trigger=data['trigger']
    
        var function
    
        if data.find('function')
            import string
            function=tools.compile.evaluate(data['function'])
        else
            logger.error(string.format('Using default function for %s',trigger))
            function=/value,data->{'value':value,'data':data}
        end

        return callback_type(trigger,/value,data->tasmota.set_timer(0,/->self.publish_output(function,value,data,topic)))
    
    end

    def close()
        self.registry_daemon.remove_all()
        self.registry_config.remove_all()
        self.downloader.close()
    end

end

mod.Daemon=Daemon
mod.daemon=nil

return mod