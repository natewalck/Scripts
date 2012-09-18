# == Synopsis
#
# scriptRunner: Runs scripts either once or every time
#
# == Usage
#
# scriptRunner.rb -o /path/to/runOnce -e /path/to/runEvery
#
# -h, --help:
#    show help
#
# --once /path/to/runOnce, -o /path/to/runOnce
#    Run scripts in 'runOnce' one time
#
#
# --every /path/to/runEvery, -e /path/to/runEvery
#    Run scripts in 'runEvery' one time
#

require 'getoptlong'
require 'rdoc/usage'

opts = GetoptLong.new(
  [ '--help', '-h', GetoptLong::NO_ARGUMENT ],
  [ '--once', '-o', GetoptLong::OPTIONAL_ARGUMENT ],
  [ '--every', '-e', GetoptLong::OPTIONAL_ARGUMENT ]
)

runOnce = nil
runEvery = nil

opts.each do |opt, arg|
  case opt
  when '--help'
    RDoc::usage
  when '--once'
    if arg.nil? || arg == '' then
      raise ArgumentError, arg + '--once argument is nil or empty'
    else
      if File.directory? arg then
        runOnce = arg
      else
        raise ArgumentError, arg + ' is not a directory'
      end
    end
  when '--every'
    if arg.nil? || arg == '' then
      raise ArgumentError, arg + '--every argument is nil or empty'
    else
      if File.directory? arg then
        runEvery = arg
      else
        raise ArgumentError, arg + ' is not a directory'
      end
    end
  end
end

puts runOnce
puts runEvery
