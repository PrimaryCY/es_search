//全局配置文件

let settings={
}

settings.DEBUG=true

if(settings.DEBUG){
  //socket的url地址
  settings.SOCKET_URL='http://127.0.0.1:8000'
  //后台url地址
  settings.SERVER_URL='http://127.0.0.1:8000'
}else {
  settings.SERVER_URL='http://192.168.105.228:8000'
  settings.SOCKET_URL='http://192.168.105.228:8000'
}


settings.TOKEN_NAME='tk'



export default settings
