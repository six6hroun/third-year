require 'logger'

class AppLogger
    def self.build(path)
        logger = Logger.new(path)
        logger.level = Logger::DEBUG
        logger.formatter = proc do |severity, datetime, _, msg|
            "#{datetime.strftime('%Y-%m-%d %H:%M:%S')} [#{severity}] #{msg}\n"
        end
        logger
    end
end