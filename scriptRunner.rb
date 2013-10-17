# == Synopsis
#
# scriptRunner: Runs scripts either once or every time
#
# == Usage
#
# scriptRunner.rb -o /path/to/run_once -e /path/to/run_every
#
# -h, --help:
#    show help
#
# --once /path/to/run_once, -o /path/to/run_once
#    Run scripts in 'run_once' one time
#
#
# --every /path/to/run_every, -e /path/to/run_every
#    Run scripts in 'run_every' one time
#

require 'getoptlong'
require 'rdoc/usage'
require 'osx/cocoa'
require 'time'

opts = GetoptLong.new(
  [ '--help', '-h', GetoptLong::NO_ARGUMENT ],
  [ '--once', '-o', GetoptLong::OPTIONAL_ARGUMENT ],
  [ '--every', '-e', GetoptLong::OPTIONAL_ARGUMENT ]
)

run_once = nil
run_every = nil

opts.each do |opt, arg|
  case opt
  when '--help'
    RDoc::usage
  when '--once'
    if arg.nil? || arg == '' then
      raise ArgumentError, arg + '--once argument is nil or empty'
    else
      if File.directory? arg then
        run_once = arg
      else
        raise ArgumentError, arg + ' is not a directory'
      end
    end
  when '--every'
    if arg.nil? || arg == '' then
      raise ArgumentError, arg + '--every argument is nil or empty'
    else
      if File.directory? arg then
        run_every = arg
      else
        raise ArgumentError, arg + ' is not a directory'
      end
    end
  end
end



if run_every then
  Dir.foreach(run_every) do |script|
    next if script == '.' or script == '..'
    script_path = File.join(run_every, script)
    if [2, 3, 6 ,7].include?(Integer(sprintf("%o", File.stat(script_path).mode)[-1,1]))
      puts "#{script_path} has dubious permissions"
    elsif !File.executable?(script_path)
      puts "#{script_path} is not executable"
    else
      system(script_path)
    end
  end
end

if run_once then
  run_once_plist = File.expand_path("~/Library/Preferences/" + "com.company.scriptrunner.plist") 
  plist_contents = OSX::NSMutableDictionary.dictionaryWithContentsOfFile(run_once_plist)
  if plist_contents == nil then
    plist_contents = OSX::NSMutableDictionary.alloc.init 
  end
  
  Dir.foreach(run_once) do |script|
    next if script == '.' or script == '..'
      if plist_contents.has_key?(script)
        puts "#{script} has already been run"
      else
        script_path = File.join(run_once, script)
        if [2, 3, 6 ,7].include?(Integer(sprintf("%o", File.stat(script_path).mode)[-1,1]))
          puts "#{script_path} has dubious permissions"
        elsif !File.executable?(script_path)
          puts "#{script_path} is not executable"
        else
          system(script_path)
          plist_contents[script] = Time.now.utc.iso8601 
        end
      end
  end
  plist_contents.writeToFile_atomically(run_once_plist,true)
end
