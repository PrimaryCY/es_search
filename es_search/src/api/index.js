import axios from './ajax'


export const search=(params)=>axios.get('api/web/search/',params)


/*
* 上传文件接口
* 请求:{file:文件对象}
* 响应:{'code':2000,'msg':'ok',url:文件存储后的url}
* */
export const upload=(data)=>axios.upload('/api/v1/upload',data)
