import sys
import sorting
import os 

path = ""
commands = []

volumes = {}

def parse_compose_file(my_path, yaml_file):
    global path
    path = os.path.basename(os.path.dirname(my_path))

    services = yaml_file['services']
    sorted_services = sorting.sort(services)

    parsed_services = []
    for d in sorted_services:
        for name, service in d.items():
            parsed_services.append(ServiceParser(name, service))

    networks = yaml_file['networks']
    for n in networks:
      if n == 'default':
        for k,v in networks[n].items():
            if k == 'external': # add this network
              commands.append("docker network create  {}".format(v['name']))
              for s in parsed_services:
                s.docker_args['network'] = " --network={} ".format(v['name'])

    volumes = yaml_file['volumes']
    for v in volumes:
        commands.append("docker volume  create  {}_{}".format(path, v))            

    for s in parsed_services:
        commands.append(s.write_run_command())
    return commands

class ServiceParser(object):
  def __init__(self, name, service):
    self.docker_args = {}
    self.name = name
    self.image = service['image'] # always has image!
    self.service = service
    self.parse()

  def parse(self):
    self.docker_args['image'] = self.image
    for arg in self.service:
      found = filter(lambda x: ("parse_" + arg) == x, dir(ServiceParser))
      if not found:
        print ("ERR parse_{} not found".format(arg))
      else:
        self.docker_args[arg] = getattr(self,"parse_"+arg)(self.service[arg])
    if 'container_name' not in self.docker_args:
      self.docker_args['name'] = self.name
    #print self.docker_args
    return self.docker_args # for compat.

  def write_run_command(self):
    command = "docker run -d "
    for arg in self.docker_args:
      if arg != 'entrypoint' and arg != 'command' and arg != 'image':
        command += self.docker_args[arg]
    command += " {} ".format(self.image)
    if 'entrypoint' in self.docker_args:
      command += ' {} '.format(self.docker_args['entrypoint'])  
    if 'command' in self.docker_args:
      command += ' {} '.format(self.docker_args['command'])
    return command

  def parse_build(self, vals):
    command = "docker build -t " + self.image
    context = vals.get('context', '.')
    if context != ".":
      commands.append("cd " + context)
    if 'dockerfile' in vals:
      command += " --file {}".format(vals['dockerfile'])
    command += " ."
    #print "com", command
    commands.append(command)
    if context != ".":
      commands.append("cd -")
      commands.append("")
    return ''

  def parse_name(self, name):
    return ' --name={}_{} '.format(path,name)

  def parse_container_name(self, name):
    return ' --name={} '.format(name)
    
  def parse_restart(self, restart):
    return '--restart={} '.format(restart)

  def parse_image(self, image):
    return image

  def parse_depends_on(self, deps):
    return to_docker_arg(deps, " --link={0} ")

  def parse_links(self, links):
    return parse_depends_on(links)

  def parse_ports(self, ports):
    return to_docker_arg(ports, " -p {0} ")

  def parse_volumes(self, volumes):
    string = ""
    for v in volumes:
      if '/' in v.split(':')[0]:
        string += "-v {} ".format(v)
      else: # named!
        string += "-v {}_{} ".format(path, v)
    return string	

  def parse_expose(self, exports):
    return to_docker_arg(exports, " --expose={0} ")

  def parse_entrypoint(self, entrypoint):
    return " --entrypoint={0} ".format(entrypoint)

  def parse_env_file(self, envfile):
    return  ' --env-file="{0}" '.format(envfile)

  def parse_environment(self, envs):
    string = ""
    if type(envs) is list:
        for k in envs:
            string += ' -e {} '.format(k)
    else:
        for k, v in envs.items():
            string += ' -e {0}="{1}" '.format(k, v)
    return string

  def parse_command(self, command):
    if type(command) is list:
        return ' '.join(command)
    else:
        return command
  

def to_docker_arg(args, str_format):
    string = ""
    for a in args:
        string += str_format.format(a)
    return string
