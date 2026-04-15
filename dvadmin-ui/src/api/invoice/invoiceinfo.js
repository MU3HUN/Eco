import request from "@/utils/request";

// 发票信息列表
export function getinvoiceinfoList(query) {
  return request({
    url: "/invoice/invoice/get_AllinvoiceList",
    method: "get",
    params: query
  });
}
// 通过orc识别发票信息，然后添加到数据库表中
export function AddinvoinceInfoByOrc(query) {
    return request({
      url: "/invoice/invoice/AddinvoinceInfoByOrc",
      method: "get",
      params: query,
      timeout: -1 // 20秒
    });
  }

  // 发票验真
export function Checkinvoince(query) {
  return request({
    url: "/invoice/invoice/Checkinvoince/" + query + "/",
    method: "get",
    timeout: -1 // 20秒
  });
}
  // 删除
  export function Delinvoince(dictId) {
    return request({
      url: "/invoice/invoice/Delinvoince/" + dictId + "/",
      method: "delete",
    });
  }
// 修改发票信息
export function editinvoice(data) {
  return request({
    url: "/invoice/invoice/editinvoice/",
    method: "put",
    data: data
  });
}
// 手动新增发票信息
export function addinvoice(data) {
  return request({
    url: "/invoice/invoice/addinvoice/",
    method: "post",
    data: data
  });
}
// 清空文件夹
export function delfile(data) {
  return request({
    url: "/invoice/invoice/delfile/",
    method: "post",
    data: data
  });
}