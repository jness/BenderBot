import socket
from time import sleep

class IRC:

    server = "irc.example.com"
    port = "6667"
    channel = "#test"
    botnick = "BenderBot"

    def connect(self):
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print '[INFO] connecting to %s:%s' % (self.server, self.port)
        self.ircsock.connect((self.server, int(self.port)))
        print '[INFO] setting nick to %s' % self.botnick
        self.ircsock.send("USER "+ self.botnick +" "+ self.botnick +" "+ self.botnick +" :Bite my shiny metal ass\n")
        self.ircsock.send("NICK "+ self.botnick +"\n")
        sleep(10)
        data = self.ircsock.recv(2048).strip('\n\r')
        if data.find("Nickname is already in use") != -1:
            print '[INFO] setting nick to %s' % self.altbotnick
            self.ircsock.send("USER "+ self.altbotnick +" "+ self.altbotnick +" "+ self.altbotnick +" :Bite my shiny metal ass\n")
            self.ircsock.send("NICK "+ self.altbotnick +"\n")
            sleep(10)
        print '[INFO] joining channel %s' % self.channel
        self.joinchan(self.channel)
        return self.ircsock

    def quit(self):
        self.ircsock.close()

    def joinchan(self, channel):
      self.ircsock.send("JOIN "+ channel +"\n")
    
    def ping(self):
      self.ircsock.send("PONG :pingis\n")

    def post(self, msg):
      self.ircsock.send("PRIVMSG "+ self.channel +" :"+ msg +"\n")

    def sendmsg(self, nick, msg):
      self.ircsock.send("PRIVMSG "+ nick +" :"+ msg +"\n")


